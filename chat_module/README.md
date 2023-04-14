# Chat-Module

Login
```
-> REST: /accounts/login
```

Redirect to Chat-Module: Specify bot_profile_id and email within get parameter. Ensure that a bot with this id and a user with this email is registered in the database.
```
-> REST: /chat-module/?bot_profile_id=<bot_profile_id>&email=<email>
```

For best experience install Node from [here](https://nodejs.org/en/download), or
```
$ brew install node
```

Empty User Profile and Chat History are created if not found.