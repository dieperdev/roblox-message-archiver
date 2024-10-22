<p align="center">
    <img src="https://images.rbxcdn.com/b3265c712cb9adef3d30b52a1711e387-roblox_logo_light_08292022.svg" height="72">
</p>

# Roblox Message Archiver

### Roblox Message Archiver is a utility to archive messages from your Roblox Inbox (and other categories). Roblox has announced that they are [removing user-to-user inbox messaging](https://devforum.roblox.com/t/sunsetting-user-to-user-inbox-messaging/3187502) via the Messages (not Chat) feature on October 29th, 2024.

#### NOTE: I will be working on a tool that will transform your messages into a browsable document. Expect this in a few weeks.

## Table of contents
- [Why you should archive your messages](#why-should-you-archive-your-messages)
- [Is this script safe?](#is-this-script-safe)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Customizing variables](#customizing-variables)
- [Running the script](#running-the-script)
- [Finding your messages](#finding-your-messages)
- [License](#license)

## Why should you archive your messages?
Roblox doesn't always act in the community's best interest. Roblox said they would make previous messages "read-only". You may lose your messages if you don't save them now as Roblox may delete them in the future without warning. It's better to be safe than sorry.

## Is this script safe?
This script is completely safe. It does not send any of your messages or your cookie anywhere besides Roblox servers. Your data remains on your device. You can look through the source code and verify this yourself.

## Prerequisites
Before you continue, you'll need to [install python](https://www.python.org/). This script should work with `python >= 3.8`. If you're on MacOS, Linux, or another Unix based system, you may need to use a package manager to install python.

## Installation
1. Clone the repo
    - Method 1 (git): `git clone https://github.com/dieperdev/roblox-message-archiver.git`
    - Method 2 (zip file): Download the repo as a zip file and extract it
2. Open the folder where you installed the repo
3. Create a virtual environment
    - Windows: `python -m venv venv`
    - MacOS/Linux (or other Unix systems): `python3 -m venv venv`
4. Activate the virtual environment
    - Windows: `./venv/Scripts/activate`
    - MacOS/Linux: `source venv/bin/activate`
5. Install dependencies
    - Windows: `pip install -r requirements.txt`
    - MacOS/Linux: `pip3 install -r requirements.txt`

## Customizing variables:
### Get your token
First, you'll need to grab your `ROBLOSECURITY` cookie. Check [this post](https://devforum.roblox.com/t/about-the-roblosecurity-cookie/2305393) on the devforum to get it. Look under the "How can I see my cookie?" section. The developer tools option is recommended.

### Editing your variables
Open `.env.example` and edit the variables in the file. You should place your cookie in the `ROBLOSECURITY` string (delete all existing text). Next, you should replace `ARCHIVE_INDIVIDUAL` with `0` or `1`. The comments in the file will guide you on which one to pick.

After the previous steps, you need to rename the `.env.example` file to `.env`.

## Running the script
- Windows: `python main.py`.
- MacOS/Linux (or other Unix systems): `python3 main.py`

## Finding your messages
Your messages can be found in the `archives` directory. Messages are named by their message id and can be found in the following folders:
- `archives/inbox`
- `archives/sent`
- `archives/news`
- `archives/archive`

There is also `inbox.json`, `sent.json`, `news.json`, and `archive.json` files in the `archive` directory that contain all the messsages in the corresponding category.

## License
### [MIT License](https://opensource.org/licenses/MIT)
