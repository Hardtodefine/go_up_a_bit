# vue2和vue3区别

### 先说显式的一些改变

- 因为改成组合式api所有没有this
- 生命周期可以用setup替代before create和created
- vue3中的v-if高于v-for的优先级
- 创建根的实例从new app变成了createApp方法
- 一些全局注册,比如mixin,注册全局组件,use改成了用app实例调用,而不是vue类调用
- 新增了teleport组件
- template模版可以不仅仅包含一个根div

### 更深层次的一些改变

- 响应式原理改用了 proxy，解决了数组无法通过下标修改，无法监听到对象属性的新增和删除的问题，也提升了响应式的效率。
- 可以额外叙述vue3并不是完全抛弃了defineProperty,通过reactive定义的响应式数据使用proxy包装出来，而ref还是用的defineProperty去给一个空对象，定义了一个value属性来做的响应式
- 组合式API的写法下，源码改成了函数式编程，方便按需引入，因为tree-shaking功能必须配合按需引入写法，所以vue3更好地配合tree-shaking能让打包体积更小
  

# Vue中的生命周期函数有哪些？它们的作用是什么？

●[beforeCreate](https://v2.cn.vuejs.org/v2/api/#beforeCreate)
●[created](https://v2.cn.vuejs.org/v2/api/#created)
●[beforeMount](https://v2.cn.vuejs.org/v2/api/#beforeMount)
●[mounted](https://v2.cn.vuejs.org/v2/api/#mounted)
●[beforeUpdate](https://v2.cn.vuejs.org/v2/api/#beforeUpdate)
●[updated](https://v2.cn.vuejs.org/v2/api/#updated)
●[activated](https://v2.cn.vuejs.org/v2/api/#activated)
●[deactivated](https://v2.cn.vuejs.org/v2/api/#deactivated)
●[beforeDestroy](https://v2.cn.vuejs.org/v2/api/#beforeDestroy)
●[destroyed](https://v2.cn.vuejs.org/v2/api/#destroyed)
●[errorCaptured](https://v2.cn.vuejs.org/v2/api/#errorCaptured)

# 请介绍一下Vue的组件化原理，以及它与传统模板驱动开发的区别？

Vue的组件化提供了几个优势:

1 可重用性:组件可以在应用程序的不同部分之间重用，从而允许您构建一致的用户界面并编写较少重复的代码。 
2 封装:Vue中的每个组件封装自己的逻辑和状态，使其更易于推理和维护。这种隔离还可以防止跨组件干扰。 
3 模块化:组件可以独立开发和测试，使开发和调试更易于管理。它还促进了团队成员之间的协作。
4 组合:Vue鼓励将组件组合在一起以创建复杂的ui。使用组件作为构建块，您可以灵活地组合它们以满足您的特定需求。 
5 更清晰的结构:将应用程序分解成组件可以创建更有组织的结构，使其更容易理解和浏览代码库。 

Vue通过它的组件系统使组件化变得更容易，比如props(将数据从父组件传递给子组件的属性)、event(从子组件传递给父组件的属性)和slot(定义灵活的内容插入点)。

总的来说，Vue的组件化促进了模块化和可重用的方法来构建用户界面，从而产生更具可维护性和可扩展性的应用程序。

# Vue中如何进行跨组件通信？请列举几种常见的方法，并简要说明它们的优缺点。

在Vue中，有几种常见的跨组件通信方法。 让我们探讨每种方法并简要说明它们的优点和缺点：

1. Props and $emit: 
   ○优点： Props 和 $emit 是父子组件之间最基本、最直接的通信方式。 父组件通过 props 将数据传递给子组件，子组件使用 $emit 发出事件来通知父组件发生的变化。
   ○缺点： 这种方法非常适合简单直接的亲子沟通。 但是，当处理深度嵌套的组件或需要在不相关的组件之间传递数据时，它可能会变得很麻烦。 在这种情况下，props 钻探（通过多个级别的组件传递 props）可能会导致代码冗长并降低可维护性。
2. Provide/Inject： 
   ○优点： provide 和 inject 功能允许您在组件中提供数据并将其注入到其子组件中，无论其嵌套级别如何。 它提供了一种在多个组件之间共享数据的便捷方法，而无需通过每个中间组件显式传递 props。
   ○缺点： 使用 provide 和 inject 会使跟踪注入数据的来源变得更加困难，因为它不会像 props 那样强制执行清晰的数据流。 这使得理解和维护代码库变得更具挑战性，尤其是在大型应用程序中。
3. Event Bus： 
   ○优点： 事件总线是专用于发出和侦听事件的 Vue 实例。 组件可以在事件总线上发出事件，其他组件可以侦听这些事件并做出相应的反应。 它提供了一个集中的通信通道，允许组件在没有直接父子关系的情况下进行通信。
   ○缺点： 使用事件总线可能会导致跟踪和理解应用程序中的事件流变得困难，尤其是当组件数量增加时。 它可能会导致清晰度下降，并且更难以推断应用程序的状态和行为。
4. Vuex (State Management)： 
   ○优点： Vuex 是 Vue.js 的状态管理模式和库。 它提供了一个集中存储来保存应用程序的状态，并允许组件通过获取器和突变来访问和修改状态。 Vuex 适合管理复杂的应用程序状态、在组件之间共享数据以及跨应用程序同步状态更改。
   ○缺点： Vuex 引入了额外的复杂性和样板代码，这对于较小的应用程序或简单的用例来说可能是过度的。 它需要一个学习曲线才能有效地理解和使用。 使用 Vuex 进行简单和本地化的组件通信可能会导致不必要的开销和复杂性。
5. this.$refs： 
   ○优点： this.$refs 允许您直接从父组件访问子组件。 您可以使用 refs 来调用方法或访问子组件的属性。 它提供了一种在父组件和子组件之间建立直接通信通道的方法，而无需道具或事件。
   ○缺点： 使用 this.$refs 可以在父组件和子组件之间创建紧密耦合，从而降低它们的可重用性并且更难以维护。 它绕过了通常的单向数据流，并可能导致代码更难以推理和测试。

每种通信方式都有自己的长处，适合不同的场景。 根据应用程序的复杂性、组件之间的关系以及所需的解耦和可维护性级别来选择适当的方法非常重要。 对于简单的父子通信，props 和 $emit 通常就足够了。 如果您有更复杂的状态管理需求或需要在不相关的组件之间共享数据，Vuex 或事件总线可能会很有用。 provide 和 inject 适合跨多个嵌套级别共享数据。 最后，必要时，this.$refs 可以方便地在父组件和子组件之间进行直接通信，但应谨慎使用以避免紧密耦合。

# **请对比解释一下Vue中的数据双向绑定与react单向数据流**

**Vue 中的双向数据绑定：**
在 Vue 中，双向数据绑定允许您在 Vue 组件中的数据和用户界面 (UI) 元素（例如输入字段、复选框等）之间建立同步。当数据更改时，UI 会自动更新，并且 反之亦然。 这意味着 UI 元素的更改会反映在底层数据中，并且数据的更改会立即反映在 UI 中。



下面是 Vue 中双向数据绑定的示例：

```html
<template>
  <div>
    <input v-model="message" type="text">
    <p>{{ message }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      message: ''
    };
  }
};
</script>

```

在此示例中，“v-model”指令在“message”数据属性和“”元素之间建立双向数据绑定。 输入字段中所做的任何更改都将更新“message”数据属性，对“message”属性的任何更改都将更新输入字段和“

”元素。



**React 中的单向数据流：**
在React中，数据流是单向的，这意味着数据从父组件向子组件单向流动。 父组件通过 props 将数据传递给子组件，子组件不能直接修改它们接收到的 props。 相反，子组件可以通过调用作为 props 传递的回调函数来请求更改，并且父组件相应地处理状态更新。



下面是 React 中单向数据流的示例：

```jsx
import React, { useState } from 'react';

function ParentComponent() {
  const [message, setMessage] = useState('');

  const handleMessageChange = (event) => {
    setMessage(event.target.value);
  };

  return (
    <div>
      <ChildComponent message={message} onMessageChange={handleMessageChange} />
      <p>{message}</p>
    </div>
  );
}

function ChildComponent(props) {
  return (
    <input value={props.message} onChange={props.onMessageChange} type="text" />
  );
}
```

在此示例中，“ParentComponent”使用“useState”挂钩管理“message”状态。 它将“message”状态作为 props 以及“handleMessageChange”回调函数传递给“ChildComponent”。 `ChildComponent` 接收 `message` 属性和 `onMessageChange` 回调作为属性，并使用它们来渲染输入字段。 当输入字段值发生变化时，会调用“onMessageChange”回调，父组件会相应更新“message”状态。

**比较：**



- **数据流向：** Vue 的双向数据绑定允许数据更改既从数据流向 UI，又从 UI 流向数据。 React 的单向数据流限制数据更改只能从父组件流向子组件。
- **易于使用：** Vue 中的双向数据绑定简化了保持 UI 和数据同步的过程，因为 UI 或数据中的更改会自动反映在另一个中。 React 中的单向数据流促进了一种更明确和可预测的数据流，这可以使应用程序的状态更改更容易理解和推理。
- **控制和灵活性：** React 中的单向数据流为数据的管理和修改方式提供了更多的控制和灵活性。 通过通过 props 显式传递数据并处理父组件中的状态更新，它可以更好地控制数据突变，并对应用程序逻辑进行更细粒度的控制。
- **性能注意事项：** React 中的单向数据流在某些情况下可以提高性能，因为它简化了跟踪和管理更改的过程。 React 的虚拟 DOM 协调算法可以根据单向数据流选择性地仅重新渲染需要更新的组件来优化更新。
- **学习曲线：** Vue 中的双向数据绑定对于初学者来说更容易掌握，因为它抽象了管理数据流的一些复杂性。 React 中的单向数据流需要更明确地理解数据如何通过 props 和回调传递和更新。



两种方法各有优势，适用于不同的场景。 Vue 的双向数据绑定对于数据流不太复杂的简单应用程序来说很方便，而 React 的单向数据流为管理更大、更复杂的应用程序中的状态提供了更多的控制和灵活性。

# 请解释一下Vue中的路由管理器(vue-router)其工作原理

Vue Router 是 Vue.js 的路由库，允许您在 Vue 应用程序中实现客户端路由。 它的工作原理是管理不同视图或组件之间的导航，无需重新加载页面，从而实现单页面应用程序 (SPA) 体验。

# Vue中的事件处理机制是怎样的？如何使用自定义事件？

在 Vue.js 中，事件处理机制允许您响应用户交互或应用程序中发生的其他事件。 Vue 提供了一种简单的方法来处理事件并使用内置事件和自定义事件在组件之间进行通信。

**内置事件处理**：Vue 提供了一组指令来处理常见的 DOM 事件，例如 click、input、submit 等。您可以直接在模板中使用这些指令来 将事件侦听器绑定到元素：

```html
<button v-on:click="handleClick">Click me</button>
```

在上面的示例中，“v-on:click”指令将“handleClick”方法绑定到按钮的“click”事件。 单击按钮时，将执行“handleClick”方法。



**自定义事件**：除了内置事件之外，您还可以创建和发出自定义事件以促进组件之间的通信。 自定义事件允许您将数据从子组件传递到父组件或触发其他组件中的操作。

要使用自定义事件，您需要执行以下步骤：



-  使用 `$emit` 方法在子组件中定义事件:

  ```js
  this.$emit('custom-event', eventData);
  ```

在上面的代码中，“custom-event”是事件的名称，“eventData”是可以随事件一起传递的可选数据。 

-  使用“v-on”指令监听父组件中的自定义事件： 

  ```html
  <child-component v-on:custom-event="handleCustomEvent"></child-component>
  ```

  在此示例中，“v-on:custom-event”指令将“handleCustomEvent”方法绑定到“child-component”发出的“custom-event”。 

  -  在父组件中定义相应的方法来处理自定义事件： 

    

    ```js
    methods: {
      handleCustomEvent(eventData) {
        // Handle the event data
      },
    }
    ```

当自定义事件发出时，将调用handleCustomEvent方法，您可以访问从子组件传递的事件数据。 

通过使用自定义事件，您可以在组件之间建立通信通道并根据需要传递数据或触发操作。 这允许在 Vue 应用程序中实现更灵活和解耦的架构。

值得注意的是，自定义事件通常用于父子通信。 如果需要在兄弟或不相关的组件之间进行通信，可以利用其他技术，例如事件总线、Vuex（Vue 的状态管理模式）或全局事件系统。

#   请解释一下Vue中的Watcher对象，以及它是如何监听数据变化的？

在 Vue.js 中，“Watcher”对象是反应性系统的一个组成部分，它允许您监视 Vue 组件中数据属性的更改。 它负责跟踪依赖关系并在观察到的数据发生变化时更新组件。

当您在 Vue 组件中定义监视程序时，您可以指定要监视的数据属性或计算属性，以及每当监视的属性发生更改时将执行的回调函数。 然后观察者会自动检测被观察属性的变化并触发回调函数。

以下是如何在 Vue 组件中定义观察者的示例：

```js
const vm = new Vue({
  data() {
    return {
      message: 'Hello',
    };
  },
  watch: {
    message(newValue, oldValue) {
      console.log(`The message changed from "${oldValue}" to "${newValue}"`);
    },
  },
});
```

在上面的示例中，“watch”选项用于为“message”属性定义一个观察器。 观察者有一个回调函数，它接受两个参数：“newValue”和“oldValue”。 每当“message”属性发生更改时，都会使用该属性的新值和旧值调用回调函数。

观察者跟踪被观察的属性和组件渲染之间的依赖关系，因此当被观察的属性发生变化时，组件会自动重新渲染以反映更新的数据。

在底层，Vue 使用一种称为“脏检查”的技术来检测监视属性的更改。 在每次组件更新期间，Vue 都会遍历组件的数据和计算属性，如果自上次更新以来其中任何一个发生更改，则会触发相应的观察者回调。

值得注意的是，观察者最常用于观察单个数据属性。 如果您需要执行更复杂的逻辑或一起监视多个属性，则可以使用计算属性或创建依赖于多个数据属性的自定义监视程序。

总体而言，Vue 中的“Watcher”对象通过监视数据属性的更改并触发组件中的必要更新，在反应性系统中发挥着至关重要的作用。

# 请解释一下Vue中的虚拟DOM和真实DOM的概念，以及它们之间的关系？

在 Vue 中，虚拟 DOM (VDOM) 是指内存中实际 DOM (RD) 的轻量级表示。 它是 Vue（和其他 JavaScript 框架）用来高效渲染和更新 HTML 元素的技术。

真正的 DOM 是浏览器对网页 HTML 结构的实时表示。 它是浏览器在屏幕上呈现的实际树结构。 真实 DOM 的处理和操作相对较慢，因为对其进行任何更改都会导致浏览器重新计算布局并重新绘制受影响的元素。

另一方面，虚拟 DOM 是代表真实 DOM 元素及其属性的 JavaScript 对象。 它是真实 DOM 的轻量级副本，存储在内存中。 与真实 DOM 相比，虚拟 DOM 的操作和更新速度要快得多。

Vue中虚拟DOM和真实DOM的关系如下：

1. 每当应用程序的数据/状态发生变化时，Vue 就会执行重新渲染过程。
2. 在重新渲染过程中，Vue 通过将新状态与先前状态进行比较来创建新的虚拟 DOM 表示。
3. 然后将更新视图的虚拟 DOM 表示与之前的虚拟 DOM 进行比较（比较过程）。 4.Vue 识别新的和以前的虚拟 DOM 之间的差异，并仅将这些更改应用于真实 DOM。
4. 然后，使用反映新更新视图所需的最小更改集来更新真实 DOM。

这种将虚拟 DOM 与真实 DOM 进行比较并仅更新必要的更改的“差异”过程称为协调。 它允许 Vue 高效地更新 DOM，减少所需的操作数量并提高性能。

通过使用虚拟 DOM，Vue 可以确保最佳的渲染和更新性能，即使是复杂且频繁变化的 UI。

# Vue中的计算属性(computed)是如何实现的，以及它的优缺点是什么？

Vue 中的计算属性是从应用程序的数据/状态派生的属性。 它们是根据其他数据属性的状态动态计算的，并提供了一种在 Vue 组件中定义复杂、可重用逻辑的方法。

要在 Vue 中实现计算属性，您可以将它们定义为 Vue 组件的计算属性对象中的函数。 这是一个例子：

```vue
computed: {
  fullName() {
    return this.firstName + ' ' + this.lastName;
  }
}
```

在上面的示例中，“fullName”是一个计算属性，它是根据“firstName”和“lastName”数据属性的值动态计算的。 每当这些数据属性发生更改时，Vue 都会自动更新“fullName”计算属性。

使用计算属性的优点：

1. **缓存**：计算属性根据其依赖关系进行缓存。 Vue 会跟踪依赖关系，如果依赖关系没有发生变化，则不会重新计算计算属性。 这种缓存机制提高了性能，尤其是在处理繁重计算或复杂操作时。

2. **反应性**：计算的属性是反应性的。 当任何依赖项发生变化时，计算属性将自动更新。 这简化了保持 UI 与数据同步的过程。

3. **代码可读性和可重用性**：计算属性提供了一种干净简洁的方式来定义从其他数据属性派生值的逻辑。 它们使您能够以更具可读性和可维护性的方式表达复杂的逻辑。 计算属性还可以跨多个组件使用，从而促进代码重用。

使用计算属性的缺点：

**每次重新渲染时的计算**：计算的属性在每次重新渲染时都会重新评估，即使它们的依赖关系没有改变。 在某些情况下，这可能是不必要的，从而导致潜在的计算浪费。

**不能用于异步操作**：计算属性本质上是同步的。 它们不能用于涉及异步任务的操作，例如进行 API 调用。 对于异步操作，您需要使用方法。

总的来说，计算属性是 Vue 中的一个强大功能，可以增强代码的可维护性和可读性。 它们提供缓存和反应性优势，但可能并不适合所有场景，特别是在处理复杂或异步操作时。

# vue3 中的setup()何时执行，VUE3 生命周期有何变化？

在 Vue 3 中，“setup()”函数是一个新功能，它取代了 Vue 2 中“beforeCreate”和“created”生命周期函数的组合。它在创建组件之前执行，允许您设置组件的 初始状态、反应属性并执行其他初始化任务。

`setup()` 函数在组件的创建阶段执行，在组件的 props 初始化之后。 它在组件的其余生命周期函数之前运行，例如“beforeMount”、“mounted”、“beforeUpdate”等。

`setup()` 函数有两个参数：`props` 和 `context`。 `props` 参数包含组件的 props，允许您在 `setup()` 函数中使用和访问它们。 `context` 参数提供对组件生命周期方法的访问，例如用于事件处理的 `emit` 和用于访问子组件的 `$refs`。

##  onBeforeUnmount() 

##  onUnmounted() 

##  onRenderTracked() 

##  onRenderTriggered() 

##  onServerPrefetch() 

# 请介绍一下Vue的组件化原理，以及它与传统模板驱动开发的区别？

Vue的组件化提供了几个优势:

1. 可重用性:组件可以在应用程序的不同部分之间重用，从而允许您构建一致的用户界面并编写较少重复的代码。 
2. 封装:Vue中的每个组件封装自己的逻辑和状态，使其更易于推理和维护。这种隔离还可以防止跨组件干扰。
3. 模块化:组件可以独立开发和测试，使开发和调试更易于管理。它还促进了团队成员之间的协作。
4. 组合:Vue鼓励将组件组合在一起以创建复杂的ui。使用组件作为构建块，您可以灵活地组合它们以满足您的特定需求。 
5. 更清晰的结构:将应用程序分解成组件可以创建更有组织的结构，使其更容易理解和浏览代码库。  Vue通过它的组件系统使组件化变得更容易，比如props(将数据从父组件传递给子组件的属性)、event(从子组件传递给父组件的属性)和slot(定义灵活的内容插入点)。 总的来说，Vue的组件化促进了模块化和可重用的方法来构建用户界面，从而产生更具可维护性和可扩展性的应用程序。

# Vue中的生命周期函数有哪些？它们的作用是什么？

●[created](https://v2.cn.vuejs.org/v2/api/#created)
●[beforeMount](https://v2.cn.vuejs.org/v2/api/#beforeMount)
●[mounted](https://v2.cn.vuejs.org/v2/api/#mounted)
●[beforeUpdate](https://v2.cn.vuejs.org/v2/api/#beforeUpdate)
●[updated](https://v2.cn.vuejs.org/v2/api/#updated)
●[activated](https://v2.cn.vuejs.org/v2/api/#activated)
●[deactivated](https://v2.cn.vuejs.org/v2/api/#deactivated)
●[beforeDestroy](https://v2.cn.vuejs.org/v2/api/#beforeDestroy)
●[destroyed](https://v2.cn.vuejs.org/v2/api/#destroyed)
●[errorCaptured](https://v2.cn.vuejs.org/v2/api/#errorCaptured)

1. beforeCreate：在实例创建之前调用，此时还没有调用 data 选项中定义的数据和 methods 方法。
2. created：实例创建完成后调用，此时已经完成了数据的观测，但是尚未挂载DOM。
3. beforeMount：挂载之前调用，此时已经完成了数据的观测，模板已经编译，但尚未挂载到页面。
4. mounted：实例已经挂载到 DOM 上后调用。在此期间可以进行 DOM 操作。
5. beforeUpdate：数据更新之前调用，发生在虚拟 DOM 打补丁之前。
6. updated：数据更新后调用，发生在虚拟 DOM 打补丁之后，此时组件已经更新完毕。
7. activated：在 keep-alive 中，激活状态时调用。
8. deactivated：在 keep-alive 中，停用状态时调用。
9. beforeDestroy：实例销毁之前调用，在此期间可以用来清理资源。
10. destroyed：Vue 实例销毁后调用，此时所有的事件监听器和子组件已经被移除，所有的绑定器和子组件也已经解绑。
11. errorCaptured：在一个子组件中捕获错误时调用，这个错误不是由子组件的错误处理程序处理的。它会在错误传播过程中被捕获并由父组件的错误处理程序处理。