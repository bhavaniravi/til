---
description: Show different message every n seconds
---

# How to Shuffle a Message in a Div in ReactJS?

1. Create a list of messages
2. Create a shuffle component with a shuffle function
3. Plug the shuffle function into the useEffect&#x20;

```
import {useState, useCallback, useEffect} from 'react';

export default function ShuffleComponent(props) {
    const [text, setText] = useState(props.default); 
    const shuffle = useCallback(() => {
        const index = Math.floor(Math.random() * props.texts.length);
        setText(props.texts[index]);
    });

    useEffect(() => {
        const intervalID = setInterval(shuffle, 5000);
        return () => clearInterval(intervalID);
    }, [shuffle])

    return(
        <div className="shuffle">{text}</div>
    )
}
```

### **Shuffle Component**

```
  const rollingTexts = [
    "text1",
    "text2"
    "text3"
  ]

<ShuffleComponent texts={rollingTexts} default={rollingTexts[0]}/>
```
