# mimbot
ギラティナ( https://github.com/SehataKuro/Giratina )の下位互換です。  
くだらないコマンドが沢山あります。  

## コマンド一覧

- ### ^effect / ^effects / ^fx  
    画像に各種エフェクトを適用します。  
    第一引数にはエフェクトの名称を、第二引数以降にはエフェクトごとのパラメータを指定します。  
    <br/>
    **【エフェクト一覧】**  
    - #### distortion / distort / dist  
        画像を様々な形に変形させます。  
        <br/>
        **[第二引数以降のパラメータ]**  
        - ##### wave / wav (振幅) (周期) (向き)  
            波形ワープ  
            "向き"にhorizontal / horと入力すると波が横向きになります。  
        - ##### vortex / vor (回転量)  
            渦(未実装)

    - #### negative / nega  
        画像のネガポジを反転します。  
        
    - #### blur  
        ブラーを適用します(未実装)  
        <br/>
        **[第二引数以降のパラメータ]**  
        - ##### box (適用量)  
            ボックスブラー  
        - ##### radial / rad (適用量) (中心座標X) (中心座標Y)  
            放射ブラー  
        - ##### directional / dir (適用量) (角度)  
            方向ブラー  
        

- ### ^help  
    コマンド一覧を表示します。
    
- ### ^kotobagari / ^ktbgr  
    コマンドを送信したチャンネルの言葉狩り機能を一時的に(次回デプロイ時まで)切り替えます。
    
- ### ^kuwagata / ^kwgt  
    フラッシュさん見て見て  
    クワガタ～
    
- ### ^kuwagata_img / ^kwgt_img  
    フラッシュさん見て見て  
    クワガタ～の画像版
    
- ### ^okuri  
    おくりさんどれだけ性欲あるの

- ### ^ping  
    Pong!と応答時間を返します。

- ### ^raika / ^aaruaika  
    Raikaさんのおもしろツイートガチャ

- ### ^removebg
    remove.bg APIを用いて画像の背景を透過します。
   
- ### ^tomb / ^grave  
    墓を作ります。
    
- ### ^uma  
    ウマ娘ガチャシミュレーター
