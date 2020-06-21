# The Flow of Commands

## WORK IN PROGRESS

```twitch
User: !command args
```

-> CommandRouter -> Routes it to specific Router class
  -> Specific Router class
     -> Pair a Specific Parser with Specific Command Class
     -> Specific Command class
     -> Specific Parser class

The return from a Command Class, Should be a Command::Result

Then the CommandRouter, will handle saving a User Event,
based on what the Specific Command class returned

What should Command classes Return

- Result

PurchaseReceipt -> What is returned from User Model
PurchaseResult(Enum) -> Possible States for a 'completed' purchase

Problems:

The User Model, is returning a PurchaseReceipt,
I think this responsibilities, belongs in the BuyerClass

EconomyRouter
  -> Buyer
     -> User Model
     -> Buyer will return a Result Object
     -> Someone else should do the Styling
