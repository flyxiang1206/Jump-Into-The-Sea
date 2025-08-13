# Jump-Into-The-Sea

仿"赤燭遊戲"混元萬劫活動的 Discord 機器人

為了滿足活動結束後，大家的跳海慾望而生

也為了沒有跳過海但想跳夷下的我

> 警告：有些已知 BUG 還沒修，以及這是我第一次寫 python，code 醜請見諒

## 流程 ( main )

* 安裝 `python`

* 安裝 Discord 套件

    ```bash
    python -m pip install -U discord.py
    ```

* 將最後一行改成換成你的機器人 token

    ```python
    client.run("你的Discord機器人token")
    ```

* 把 channel_id 換成你要指定的 Discord channel_id

    ```
    channel_id = 0000000000000000
    ```

* 至 `message.csv` 新增你自己的跳海訊息

* 更換你的國家狀態圖 `CountryState.png`

* 啟動，大功告成

    ```
    python main.py
    ```

## 唯一 `message_id` 版本 ( main_edit )
> 穩定版本，基本上不會死

* 安裝 `python`

* 安裝 Discord 套件

    ```bash
    python -m pip install -U discord.py
    ```

* 把 discord_token 換成你的機器人 token

    ```python
    discord_token = ""
    ```

* 把 channel_id 換成你要指定的 Discord channel_id

    ```
    channel_id = 0000000000000000
    ```

* 把 message_id 換成你自己事先送出的訊息 ID
    ```
    message_id = 0000000000000000
    ```

* 至 `message.csv` 新增你自己的跳海訊息

* 更換你的國家狀態圖 `CountryState.png`

* 啟動，大功告成

    ```
    python main_edit.py
    ```

## 結語

### 感謝赤燭遊戲提供這次活動
### ☀️ 以太陽為名，向大道而行 🙏🏻

## 已知錯誤

* Discord 連線會莫名中斷，導致交互失敗，目前不確定原因
    > 暫時認定是 `discord.ui.view` timeout，已嘗試修正持續觀察中    
    
    > 直接改 main_edit 就可以換個方式解決

* CSV 檔資料未滿三個元素時程式會錯誤
    > 目前沒考慮修這個