# List of all commands and how to use them

## User related commands

__Show the Streamlords__
 - command: `!streamlords`

 - output: `shows a list of the streamlords in the chat`

__Check your information:__
 - command: `!me`

 - output: `beginbotbot: @<Username> - Mana:  | Street Cred: 1 | Cool Points: 1 | Wealth: 245539 | Insured: <boolean> | https://mygeoangelfirespace.city/<Username>.html`


__Show the information for a command/User:__
- command: `!perms <Command>/<User>`

- output for Command: `beginbotbot: !clap | Cost: 1 | Health: 5 | Like Ratio 100% | https://mygeoangelfirespace.city/commands/clap.html`

- output for User: `beginbotbot: @<Username> - Mana:  | Street Cred: 1 | Cool Points: 1 | Wealth: 245539 | Insured: <boolean> | https://mygeoangelfirespace.city/<Username>.html`



__Give a command to another user:__

- command: `!give <Command> <other_user>`
    - This command will transfer the command to the other user with no effect on the cost of the sound
                    
- command: `!transfer <Command> <other_user>`
    - This command will transfer the command to the other user with no effect on the cost of the sound

- command: `!donate <other_user>`
    - This command will transfer all commands to the other user with no effect on the cost of the sound

- output:   `beginbotbot: @<other_user> now has access to <Command>`
            `beginbotbot: @<User> lost access to <Command>`


- command: `!share <Command> <other_user>`
    - This command share the sound with another user
    - It will cost the user the price of the command (in CoolPoints) to share the sound
    - the sound will then cost tripple the value

- output: `beginbotbot: <User> shared <other_user> now has access to <Command>`

__Take commands from other users:__

 - command: `!steal <Command> <other_user>`
    - This command tries to take a command from another user
    - This command costs Mana
    - If sucessful, the price of the command doubles

 - output:
    - sucessful: `beginbotbot: <user> stole from <other_user>. Chance of Getting Caught: some%`
    - un-sucessful: `beginbotbot: <user> WAS CAUGHT STEALING! Chance of Getting Caught: some%. Num Attempts: 0 `
    - insurance: `beginbotbot: <user> was blocked by <other_user>'s insurance! Num Attempts: 0`

__Insurance company__

 - command `!insurance`
    - This command give you security from 1 steal attempt.
    - This command costs CoolPoints
    - You can only have 1 insurance
    - You can re-buy insurance after an attempt of stealing has failed

 - output: `beginbotbot: <User> thank you for purchasing insurance`



## Sound related commands


__Buy a command from the Begin Market:__

 - command: `!buy <Command>`
    - This command buys the requested sound at the advertised price
    - This command costs CoolPoints
    - The price of the command increases by 1

- command: `!buy random`
    - This command buys a random sound at the advertised price
    - This command costs CoolPoints
    - The price of the command increases by 1

- command: `!buy random x`
    - This command buys a  x random sounds at the advertised price if you have enough CoolPoints
    - This command costs CoolPoints
    - The price of each command increases by 1


  __Use a command you bought from the Begin Market:__ 
  
  - command: `!<Command>`

  - output: `none, sound is played on the stream`

  
__Create a command for the Begin Market:__

 - command: `!soundeffect <URL suitable for YoutubeDL> <CommandName(without ! )> <start time> <end time>`
    - This then has to be aproved by a streamlord or BeginBot himself
    - You get this sound once it is approved
    - Starting cost for all sounds is 1

## CSS based commands

__Add css to your website:__

 - command: `!css <RAW link to hosted css file>`
    - This must be the Raw link to the css file, not the default link
    - A template is available from one of the bots in the chat (just ask)
    - The css is uploaded to your site on the next website build cycle

__Homepage CSS:__

- command: `!bestcss <User>`
    - This command votes for that users css to be used on the Homepage
    - The user with the most votes controls the css of the Homepage


## The Coup system

### La_Libre
 - command: `!la_libre`
    - This is the newspaper that shows the current votes in the coup system and the cost of the coup

 - sample output: `beginbotbot: PowerUpL La Libre PowerUpR | Total Votes: 16 | Peace Count: 2 / 3 | Revolution Count: 14 / 3 | panicBasket Coup Cost: 216`

### Fence sitters
 - This is not a good place to be in any case.
    - If a revolution coup happens you will lose all
    - If a peace coup happens you will lose all your sounds

### Revolution
 - command: `!revolution`

    - If a revolution coup happens:
        - all sounds are taken and redistributed between the revolutionaries 
        - everyone else loses their stuff
    - If a peace coup happens:
        - you lose all your sounds and money
### Peace
 - command: `!peace`

    - If a revolution coup happens:
        - all sounds are taken and redistributed between the revolutionaries 
        - everyone else loses their stuff
    - If a peace coup happens:
        - Everyone on the peace side keeps their stuff
        - Everyone else loses their sounds 
        - Fence sitters keep their money
