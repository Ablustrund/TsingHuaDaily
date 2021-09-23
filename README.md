# Safety TsingHua 平安清华

使用GitHub Actions实现的清华大学全自动打卡程序。

## Quick Start
1. Fork the repository
2. Configure Secret
   Add the following message in Settings - Secret:
   - USERNAME: TsingHua UID.
   - PASSWORD: TsingHua UID password.
3. edit the [work.yml](./.github/workflow/work.yml) - `cron` to set your favorite time (UTC). Please refer to [this file](https://docs.github.com/en/actions/learn-github-actions/events-that-trigger-workflows#scheduled-events) for more details.
4. Turn on Workflow
   In the page of Actions: 
   - Turn on Workflows.
   - Select the `TsingHua Daily` workflow and enable workflow.

## Information
- The script will use the location information of the previous day when clocking in.
- The script has not been fully tested and the final effect is not guaranteed. Please use it as appropriate.
- The information provided on this website is for reference only.
- Neither the website nor its employees shall be liable to the user or any other person directly or indirectly for any error, inaccuracy or error in the transmission or transmission of any information in any way.
- To the extent permitted by law, this website hereby declares that it will not bear any direct, indirect, incidental, subordinate, special, punitive or punitive damages caused by the user or any person's use or failure to use the information or any link or item provided by this website (including but not limited to income, loss of expected profits or lost business, unrealized expected savings).
- If the information provided by this website is used or distributed to any person in any jurisdiction, which will violate the provisions of the laws or regulations of that jurisdiction, or cause this website or its third-party agent to be subject to any regulatory provisions in that jurisdiction, such information should not be used or distributed to any person in that jurisdiction To any such person. The user must ensure that it will not be subject to any local regulations that restrict or prohibit the user from using or distributing the information provided on this website.
- The copyright statement of pictures and words on this website, because the website can be uploaded by registered users, this website cannot identify the intellectual copyright of the uploaded pictures or words. If it is infringed, please inform us in time, and this website will be deleted in time.
