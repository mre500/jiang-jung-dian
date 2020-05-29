# Jiang-Jung-Dian Demo
A simple [demo](website) for AWS hackathon.


# Prerequisites
- Python >= 3.7
- R >= 3.6.1

# Setup
- `$ pip install -r requirements.txt` to install all dependencies wirtten in python. 
- To install all dependencies wirtten in R: 
    - `$ install.packages("data.table")`
    - `$ install.packages("dplyr")`
    - `$ install.packages("shiny")`
    - `$ install.packages("DT")`
    - `$ install.packages("shinydashboard")`
    - `$ install.packages("stringr")`

# Execute
1. First, run `$ python ui.py`, a GUI will pop up. \
     ![](./ui.PNG) 
     
2. Then do enrollment:
    - Enter "speaker's name" in `使用者名稱`
    - Click `開始錄音` to start enroll the speaker's voice.
    - Click `結束錄音` if one finished recording. 
    - Iterate over the first three processes if there are multiple speakers. 
    - After all speakers are enrolles, click `開始辨識`. 
3. Secondly, do recoding by clicking `會議錄音` to start recoding and clicking `結束會議` to finish recording.  

# Processes behind the scene
![](./structure.PNG)

# Result
![](./result_with_shinny.png)

# Acknowledgments
Thanks [Hack For Good](https://awstaiwanhackathon2020.splashthat.com/) hold by AWS for providing the AWS Services including Amazon Transcribe and Amazon Comprehend. 
Special thanks to Chen, Stuart, one of Solutions Architects at Amazon Web Services (AWS), for technical supports.  
