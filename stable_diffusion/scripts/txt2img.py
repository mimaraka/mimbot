import os, sys
sys.path.append('stable_diffusion')
import torch
import numpy as np
import random
from omegaconf import OmegaConf
from PIL import Image
from tqdm import tqdm, trange
from einops import rearrange
from pytorch_lightning import seed_everything
from torch import autocast
from contextlib import contextmanager, nullcontext

from ldm.util import instantiate_from_config
from ldm.models.diffusion.ddim import DDIMSampler
from ldm.models.diffusion.plms import PLMSSampler
from ldm.models.diffusion.dpm_solver import DPMSolverSampler

CONFIG_PATH = "stable_diffusion/configs/stable-diffusion/v1-inference.yaml"
AV3_CKPT = "Anything-V3.0.ckpt"
MODEL_DIR = "stable_diffusion/models"
OUT_DIR = "stable_diffusion/outputs/txt2img-samples"


def load_model(ckpt, config = OmegaConf.load(CONFIG_PATH), models=None, verbose=False):
    ckpt_path = f"{MODEL_DIR}/{ckpt}"
    assert os.path.isfile(ckpt_path)
    print(f"Loading model from {ckpt_path}")
    pl_sd = torch.load(ckpt_path, map_location="cpu")
    if "global_step" in pl_sd:
        print(f"Global Step: {pl_sd['global_step']}")
    sd = pl_sd["state_dict"]
    model = instantiate_from_config(config.model)
    m, u = model.load_state_dict(sd, strict=False)
    if len(m) > 0 and verbose:
        print("missing keys:")
        print(m)
    if len(u) > 0 and verbose:
        print("unexpected keys:")
        print(u)

    model.cuda()
    model.eval()

    models_ = models if models else {}

    if not ckpt in models_.keys():
        models_[ckpt] = model

    return models_


def txt2img_proc(
    prompt,
    negative_prompt="",
    outdir=OUT_DIR,
    filename="",
    ckpt="",
    sampling_method="ddim",
    n_samples=1,
    n_iter=1,
    sampling_steps=24,
    seed=-1,
    width=512,
    height=512,
    models=None
):
    fixed_code = False
    precision = "autocast" # "full" or "autocast"
    C = 4
    f = 8
    scale = 7.5
    ddim_eta = 0.0

    if seed < 0:
        sd = random.randrange(0, 4294967295, 1)
    else:
        sd = seed

    ckpt_path = f"{MODEL_DIR}/{ckpt}"
    assert os.path.isfile(ckpt_path)
    seed_everything(sd)

    config = OmegaConf.load(CONFIG_PATH)
    mds = load_model(ckpt, config=config, models=models) if not models else models

    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    md = mds[ckpt].to(torch.float16).to(device)

    if sampling_method == "dpm_solver":
        sampler = DPMSolverSampler(md)
    elif sampling_method == "plms":
        sampler = PLMSSampler(md)
    else:
        sampler = DDIMSampler(md)

    os.makedirs(outdir, exist_ok=True)

    batch_size = n_samples
    assert prompt is not None
    data = [batch_size * [prompt]]
    assert negative_prompt is not None
    data_nega = [batch_size * [negative_prompt]]

    base_count = len(os.listdir(outdir))

    start_code = None
    if fixed_code:
        start_code = torch.randn([n_samples, C, height // f, width // f], device=device)

    precision_scope = autocast if precision=="autocast" else nullcontext
    with torch.no_grad():
        with precision_scope("cuda"):
            with md.ema_scope():
                for _ in trange(n_iter, desc="Sampling"):
                    for prompts, negative_prompts in zip(tqdm(data, desc="data"), data_nega):
                        uc = None
                        if scale != 1.0:
                            if isinstance(negative_prompts, tuple):
                                negative_prompts = list(negative_prompts)
                            uc = md.get_learned_conditioning(negative_prompts)
                        if isinstance(prompts, tuple):
                            prompts = list(prompts)
                        c = md.get_learned_conditioning(prompts)
                        shape = [C, height // f, width // f]
                        samples_ddim, _ = sampler.sample(S=sampling_steps,
                                                         conditioning=c,
                                                         batch_size=n_samples,
                                                         shape=shape,
                                                         verbose=False,
                                                         unconditional_guidance_scale=scale,
                                                         unconditional_conditioning=uc,
                                                         eta=ddim_eta,
                                                         x_T=start_code)

                        x_samples_ddim = md.decode_first_stage(samples_ddim)
                        x_samples_ddim = torch.clamp((x_samples_ddim + 1.0) / 2.0, min=0.0, max=1.0)
                        x_samples_ddim = x_samples_ddim.cpu().permute(0, 2, 3, 1).numpy()

                        x_image_torch = torch.from_numpy(x_samples_ddim).permute(0, 3, 1, 2)

                        for x_sample in x_image_torch:
                            x_sample = 255. * rearrange(x_sample.cpu().numpy(), 'c h w -> h w c')
                            img = Image.fromarray(x_sample.astype(np.uint8))
                            img.save(os.path.join(outdir, f"{filename if filename else base_count:05}.png"))
                            base_count += 1

    print("Succeed to generate.")
    return sd