import { useState } from "react";

export default function Button({ children }) {
  const [count, setCount] = useState(0);
  const add = () => setCount(count + 1);
  const subtract = () => setCount(count - 1);

  return (
    <>
      <div className="flex items-center gap-2">
        <button onClick={subtract} className="btn">
          -
        </button>
        <pre>{count}</pre>
        <button onClick={add} className="btn">
          +
        </button>
      </div>
      <div>{children}</div>
    </>
  );
}
