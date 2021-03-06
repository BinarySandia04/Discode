# Discode
## What is Discode?
Discode is a Discord Bot capable of executing code inside Discord itself.
Currently Discode is compatible with these languages:
- ~~Python~~
- C++
## Bot usage
### Help message
The help message can be displayed with `!dc`. The help
message is directly read from the `help.txt` file.
### Admin commands
This commands work if your Discord user id matches with the one specified in the `ADMIN_ID` global variable inside the bot's code:
. `!dc run` Runs code

- `!dc servers` Displays info about the guild that this bot is currently in
- `!dc c` Gets info of the last commit to this github repository
- `!dc r` Executes `git fetch` and `git pull` and then the bot automatically restarts.
## Code execution
You can execute code using different prefixes stablished inside the `PREFIX` global variable. If you want to execute code inside Discord your message must follow these structures:
### C++
```cpp
    ```cpp
    #include <iostream>
    using namespace std;
    int main(){
        cout << "This is cool!" << endl;
    }
    ```
```
### Python
```py
    ```py
    print("This is also cool!")
    ```
```
Then you need to send the command `!dc run`

Discode is also capable of managing de std::cin buffer, so you are able to do commands like `input()`, `std::cin` or `std::getline`. If you send a text message while Discode is running your code, it will pass the content of the message directly to your program.
