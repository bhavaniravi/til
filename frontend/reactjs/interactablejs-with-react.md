# InteractableJS with React

When building 100Ideas project and it's board view where you can drag and drop ideas around the div I wanted to use [interact.js](https://interactjs.io/). The project though was in plain JS. I tried a few codesandbox examples that ports it to React, but it didn't work for me in the project. This writeup is a compilation of every hiccup I faced when building this drag and drop UI and how I over came it.

> I didn't come up with all of this on my own, most of this is from [interact.js](https://interactjs.io/) documentation and [codesandbox](https://codesandbox.io/s/xl4qqqn774?file=/src/styles.css:37-279) of [George Gray](https://github.com/mrgeorgegray)

### The Goal

{% embed url="https://youtu.be/Zxinb8anAGo" %}
The goal is to have div with multiple Items and ability to move them around
{% endembed %}

### Project Setup

For this setup you can create a project with `create-react-app` with three files as following

```
src
  |_ App.js
  |_ Interactable.js
  |_ App.css
```

### Draggable Items

Let's create a div with draggable Items first later we can hook in the listeners to it.

{% code title="App.js" %}
```jsx
export default function App() {
    return (
      <div className="App" id="App">
          <div className="draggable drag-item">
            <p>Drag Item 1</p>
          </div>

          <div className="draggable drag-item">
            <p>Drag Item 2</p>
          </div>
      </div>
    );
}
```
{% endcode %}

### CSS

**\*\*Important\*\***

CSS in this case is not just to style the div but also to set the start position to (0, 0)

```css
.drag-item {
  width: 5%;
  height: 100%;
  min-height: 6.5em;

  background-color: #29e;
  color: white;

  border-radius: 0.75em;

  -webkit-transform: translate(0px, 0px);
  transform: translate(0px, 0px);
}
```

### Pure JS Way

As I mentioned before for some reason, I couldn't implement the interactable logic in React way with components, so I went with a pure JS way.

For this we need to first install `interactablejs` package

```
npm install interactablejs
```

Next we are going to hook the `interact` function of this package to all the `dragItem` div

{% code title="Interactable.js" %}
```jsx
import interact from 'interactjs'

// target elements with the "draggable" class
interact('.draggable')
  .draggable({
    inertia: false,
    // Ensures the element stays with in the parent div
    modifiers: [
      interact.modifiers.restrictRect({
        restriction: '#App',
        endOnly: true
      })
    ],
    // enable autoScroll
    autoScroll: false,

    listeners: {
      // this function is called when card is moved
      move: dragMoveListener,
    }
  })

```
{% endcode %}

### Listener to Move the Card

Unlike what I thought the logic to move the card was rather simple, look for yourself

{% code title="Interactable.js" %}
```jsx
const draggableOptions = {
  onmove: event => {
    // the element we are moving
    const target = event.target;
    // Add the relative position to current position of the div
    const x = (parseFloat(target.getAttribute("data-x")) || 0) + event.dx;
    const y = (parseFloat(target.getAttribute("data-y")) || 0) + event.dy;

    // translate the element to new position
    target.style.webkitTransform = target.style.transform =
      "translate(" + x + "px, " + y + "px)";

    // update the posiion attributes
    target.setAttribute("data-x", x);
    target.setAttribute("data-y", y);
    
    // These two lines is very important for the next section
    event.stopImmediatePropagation();
    return [x, y]
  }
};
```
{% endcode %}

### ReactJS Way

This is an alternative to the Pure JS way. If the pure js way works fine why would we need the ReactJS way? Here's why?

* React works with states and components&#x20;
* The position of a dragItem is technically a state that changes
* In pure JS way we have no way of tracking the changes to this state. So what?
* Let's say you want to store the items and it's associated position in a DB or send via an API call, the app compoent will have no way of knowing the current position
* Hence we need a component that can track the position. We call this the ineteractable component

#### Creating Interactable Component

Interactable is a custom component that we are going to introduce that will help us track the positions. The listener remains the same, but instead of hooking it directly to the `interact` method we will hook it to our custom component

```jsx
import interact from "interactjs";
import { Component, cloneElement } from "react";
import PropTypes from "prop-types";
import { findDOMNode } from "react-dom";

export default class Interactable extends Component {
  static defaultProps = {
    draggable: true,
    // preparing an object to hook the listener, this is the format supported by interact.js
    draggableOptions: {onmove: dragMoveListener},
  };

  render() {
    return cloneElement(this.props.children, {
      ref: node => (this.node = node),
      draggable: false
    });
  }

  componentDidMount() {
    // wrapping the component in interact method 
    this.interact = interact(findDOMNode(this.node));
    // hooking the listener in
    this.interact.draggable(this.props.draggableOptions);
  }
}

Interactable.propTypes = {
  children: PropTypes.node.isRequired,
  draggable: PropTypes.bool,
  draggableOptions: PropTypes.object,
  dropzone: PropTypes.bool,
  dropzoneOptions: PropTypes.object,
  resizable: PropTypes.bool,
  resizableOptions: PropTypes.object
};
```

That's our `Interactable` component. It does nothing but takes the element it's wrapped with and make it draggable. Let's take it back to our original App.js where we will track the position as a state

### Making Div's Interactable

Notice how the elements are wrapped with interactable component.

{% code title="App.js" %}
```jsx
import Interactable from './Interactable'

export default function App() {
    return (
      <div className="App" id="App">
          <Interactable>
            <div className="draggable drag-item">
              <p>Drag Item 1</p>
            </div>
          </Interactable>
          
          <Interactable>
            <div className="draggable drag-item">
              <p>Drag Item 2</p>
            </div>
          </Interactable>
      </div>
    );
}
```
{% endcode %}

The code will work absolutely fine at this point as well, but our goal is to persist the position of the cards at the App level. To do that we need to introduce a data structure to store the card data

```jsx
App.propTypes = {
  data: PropTypes.shape({
      id: PropTypes.shape({
          text: PropTypes.string,
          position: PropTypes.shape({
              x: PropTypes.number,
              y: PropTypes.number,
          })
      })
  }),
};
```

Update the App component to work with the props

```jsx
import './App.css';
import {useState} from 'react';

function App() {
  const [count, onChangeCount]=useState(100);
  const [data, setCurrentData] = useState({});
  
}
```

