# OurVacation

🌴🍹🍉⛱️🥥✈️⛱️🌞🏝️🌞🤩🥳
## OurVacation is a python tool kit help you to automate tedious application process.

Stress associated with job searching and application process is an unnecessary burden for Homo sapiens.[reference ?] This software tool, YourHolidy, will try to help you fill some information according to what is given to it. The goal is to reduced the fatigue, by reducing the amount of ctrl+c and ctrl+v applicants press, aslo mouse clicks. While not reducing the time used during the application process, preliminary experiments have shown that the fatigue reduced by adopting the tool is significant, after getting used to the interface. 

It is *mostly* a useful tool now, but it needs more work to make it a *good* tool. Looking forwared to collaboration, any collaboration!

## Dependencies

Too many dependencies could lead to to difficulty for future development. So I try to use third party dependencies only when necessary. Conda should take care of it if following the step.sh file.

| Tool    | Version     |
| ------- | ----------- |
|Python   | **3.10.13**   |
|selenium    | **4.16.0**   |
|webdriver-manager| **4.0.1**|

## Before using it, be sure to:
1. Write 'config.py', 'education.csv' and 'work_experience.csv' according to the format in the corresponding '_example' files.

Note the csv files are actually not comma(,) seperated. We use semicolon(;) as delimiter here so we can use comma in the text.
