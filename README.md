# Local Jupyter notebook

Execute following commamd:

```shell
docker-compose up
```

This will take a bit of time to pull jupyter image, then prompts a web link like this:

```
http://127.0.0.1:8888/?token=$SOME_TOKEN_GIBBERISH
```

Open this link in browser, use `victor.ipynb` as an example notebook that imports modules.

Go on and solve the challenge!


#  Galaxy notes

## Message 38

Message #38 describes the "interact" function: 
https://message-from-space.readthedocs.io/en/latest/message38.html

> Is a function that takes an “interaction-protocol”, some data (maybe “protocol” dependent), and some pixel. 
> It returns some new data, and a list of pictures.

```
ap modem x0 = ap dem ap mod x0
ap ap f38 x2 x0 = ap ap ap if0 ap car x0 ( ap modem ap car ap cdr x0 , ap multipledraw ap car ap cdr ap cdr x0 ) ap ap ap interact x2 ap modem ap car ap cdr x0 ap send ap car ap cdr ap cdr x0
ap ap ap interact x2 x4 x3 = ap ap f38 x2 ap ap x2 x4 x3
```

my note:

```
ap ap ap interact x2 x4 x3 = ap ap f38 x2 ap ap x2 x4 x3
ap ap ap interact x2 x4 x3 = ap ap f38 x2 ap ap x2 x4 x3
ap ap ap interact x2 x4 x3 = ap (ap f38 x2) (ap (ap x2 x4) x3)

ap ap f38 x2 x0 : is a definition how to apply galaxy
```

2nd line explains how to wrap the galaxy function to run it

We need to run galaxy on "x2 := state" and "x0 := (0, 0)"
See more details in message #39: https://message-from-space.readthedocs.io/en/latest/message39.html

3rd line tells how to use interaction in a special way


Mathematical notation:

```
// mathematical function call notation
f38(protocol, (flag, newState, data)) = if flag == 0
                then (modem(newState), multipledraw(data))
                else interact(protocol, modem(newState), send(data))
interact(protocol, state, vector) = f38(protocol, protocol(state, vector))
```

Run with galaxy:

```
interact(galaxy, state, vector) = f38(galaxy, galaxy(state, vector))
```

Okay, so we need to run `galaxy` with `state` and `vector` and then properly process the results

`galaxy(state, vector)` is expected to return `(flag, newState, data)` which could be used to do new iterations


## Message 39

> Start the protocol passing nil as the initial state and (0, 0) as the initial point. 
> Then iterate the protocol passing new points along with states obtained from the previous execution.

```
interact
ap ap ap interact x0 nil ap ap vec 0 0 = ( x16 , ap multipledraw x64 )
ap ap ap interact x0 x16 ap ap vec x1 x2 = ( x17 , ap multipledraw x65 )
ap ap ap interact x0 x17 ap ap vec x3 x4 = ( x18 , ap multipledraw x66 )
ap ap ap interact x0 x18 ap ap vec x5 x6 = ( x19 , ap multipledraw x67 )
```


This is the first line how we should run the galaxy:

```
ap (ap (ap interact x0) nil) (ap (ap vec 0) 0) = ( x16 , ap multipledraw x64 )

x0 -> x2 (flag)
nil -> x4 (empty state)
(ap ap vec 0 0) -> x3 point: (0, 0)
```

## Message 42

https://message-from-space.readthedocs.io/en/latest/message42.html

> We believe that this message tells us to run an interaction protocol called galaxy. 
> This protocol is defined in the last line of the huge message included on this page.


## Messages 40, 41

This meesages shows examples of using protocol:

```
:67108929 = ap ap b ap b ap ap s ap ap b ap b ap cons 0 ap ap c ap ap b b cons ap ap c cons nil ap ap c cons nil ap c cons
statelessdraw = ap ap c ap ap b b ap ap b ap b ap cons 0 ap ap c ap ap b b cons ap ap c cons nil ap ap c ap ap b cons ap ap c cons nil nil
```


