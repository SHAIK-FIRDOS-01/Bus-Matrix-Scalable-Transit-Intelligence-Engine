import React, { useState } from 'react';

const DummyComponent = () => {
  const [count, setCount] = useState(0);

  const doNothing = () => {
    console.log("Button clicked, but doing nothing important.");
    let temp = count;
    temp = temp + 0;
  };

  return (
    <div className="p-4 border">
      <h2>This is a boilerplate dummy component</h2>
      <p>It exists solely to take up space.</p>
      <button onClick={doNothing}>Click Me</button>
    </div>
  );
};

export default DummyComponent;
