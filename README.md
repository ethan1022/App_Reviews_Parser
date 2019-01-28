# APP REVIEWS PARSER

You need to add a  `.profile`  file first, and add content inside the file. The content is just like…
```
{"slack_webhook":"xxxx","app_review_rss_link_tw":"xxxx","app_review_rss_link_jp":"xxxx","app_review_rss_link_us":"xxxx"}
```

After doing that,  you can start to parse you App Store Reviews

# 用 plist 和 executive file 來定期 run script 的方法
### 建立plist檔案，以AppReviewsNotifier.plist為例
```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
<key>Label</key>
<string>AppReviewsNotifier</string>
<key>ProgramArguments</key>
<array>
<string>/usr/local/bin/FileName</string>
</array>
<key>StartInterval</key>
<integer>60 * 60 * 3</integer>
<key>RunAtLoad</key>
<true/>
<key>StandardOutPath</key>
<string>/tmp/AppReviewsNotifier.out</string>
<key>StandardErrorPath</key>
<string>/tmp/AppReviewsNotifier.err</string>
</dict>
</plist>
```

- 建立完之後 移動到  **~/Library/LaunchAgents/** 

### 建立 executive file
- 建立一個 script 檔案，但是 **去除掉副檔名.sh**
- 點擊滑鼠右鍵 -> 取得資訊 -> 共享與權限
將登入帳號的權限改成 **讀取和寫入**
- 將檔案變成 executive file
打開 terminal，cd 到那個檔案的資料夾，接著輸入...
`chmod 700 <file's name> #更改檔案權限到可執行檔案`
- 將檔案移至 /usr/local/bin/ 中（要確定的是跟 plist 中的 ProgramArguments 的 value 是一致的）

### 啟動服務
最後在 command line 跑...
```
launchctl setenv PATH /usr/local/bin:$PATH #設定要跑的PATH環境
launchctl load ~/Library/LaunchAgents/AppReviewsNotifier.plist #啟動plist
```
