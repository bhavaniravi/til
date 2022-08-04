# ES6 Export vs Export Default

Export is introduced in ES6. It lets you export functions, objects, classes, or expressions from script files or modules. You export the items in one JS module to import them into multiple other modules. It enables code reusability

There are two ways you can export&#x20;

1. Named export
2. Default export

### Named Export

Let's start with a JS utils file that contains functions and classes to be reused by other modulexport function stringFormatter(text){

{% code title="utils.js" %}
```javascript
    return text.replace(" ", "_")
}

export class Wrapper{    
    
}
```
{% endcode %}

And to import this into another module, you have to mention them by their name

{% code title="app.js" %}
```javascript
import {stringFormatter, Wrapper} from './utils'
```
{% endcode %}

### Default Export

* There can be only one default export per module
* Default exports can be renamed in the importing file

{% code title="utils.js" %}
```javascript
export function stringFormatter(text){
    return text.replace(" ", "_")
}

export default class Wrapper{    
    
}
```
{% endcode %}

{% code title="app.js" %}
```
import {stringFormatter, Wrapper} from './utils'
import Wrapper, {stringFormatter} from './utils'
import WrapperNameChanged from './utils'
```
{% endcode %}

All the above statements are valid
