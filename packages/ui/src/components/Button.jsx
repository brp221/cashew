import { createSignal } from "solid-js";

export default function Button({ children }) {
  const [count, setCount] = createSignal(0);
  const add = () => setCount(count() + 1);
  const subtract = () => setCount(count() - 1);

  return (
    <>
      <div class="counter">
        <button
          onClick={subtract}
          class="py-2 px-4 bg-purple-500 text-white font-semibold rounded-lg shadow-md hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-400 focus:ring-opacity-75"
        >
          -
        </button>
        <pre>{count()}</pre>
        <button
          onClick={add}
          class="py-2 px-4 bg-purple-500 text-white font-semibold rounded-lg shadow-md hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-400 focus:ring-opacity-75"
        >
          +
        </button>
      </div>
      <div class="counter-message">{children}</div>
    </>
  );
}
