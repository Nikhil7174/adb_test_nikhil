import { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [todos, setTodos] = useState([]);
  const [todoText, setTodoText] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    fetchTodos();
  }, []);

  const fetchTodos = async () => {
    try {
      const response = await fetch('http://localhost:8000/todos');
      if (!response.ok) throw new Error('Failed to fetch TODOs');
      const data = await response.json();
      setTodos(data.todos);
      setError('');
    } catch (err) {
      setError('Failed to load TODOs. Please try again later.');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!todoText.trim()) {
      setError('Please enter a TODO description');
      return;
    }

    try {
      const response = await fetch('http://localhost:8000/todos/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ description: todoText }),
      });

      if (!response.ok) throw new Error('Failed to create TODO');
      
      setTodoText('');
      await fetchTodos();
      setError('');
    } catch (err) {
      setError('Failed to add TODO. Please try again.');
    }
  };

  return (
    <div className="App">
      <div>
        <h1>List of TODO</h1>
        {error && <p className="error">{error}</p>}
        <ul>
          {todos?.map((todo) => (
            <li key={todo.id}>{todo.description}</li>
          ))}
        </ul>
      </div>

      <div>
        <h1>Create a ToDo</h1>
        <form onSubmit={handleSubmit}>
          <div>
            <label htmlFor="todo">ToDo: </label>
            <input
              type="text"
              id="todo"
              value={todoText}
              onChange={(e) => setTodoText(e.target.value)}
              aria-label="Todo input"
            />
          </div>
          <div style={{"marginTop": "5px"}}>
            <button type="submit">Add ToDo!</button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default App;
