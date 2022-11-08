# 运行case时
 - ## 获取项目绝对路径eg（ E:\pythonProject\webPO），cmd运行
 - ### 运行单条case
 - 输入 robot  --pythonpath  项目绝对路径  --test  具体的case  case所在文件夹
   - 比如：在loginCase目录下cmd：robot  --pythonpath  E:\pythonProject\webPO   --test login_testcase_01   loginTest.robot  
 - ### 运行某个robot文件
 - 输入 robot  --pythonpath  项目绝对路径  具体的robot文件
   - 比如：在loginCase目录下cmd：robot  --pythonpath  E:\pythonProject\webPO   loginTest.robot