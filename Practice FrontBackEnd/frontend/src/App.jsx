import {useState} from 'react';
import api from './api';

function App() {
  const [salary, setSalary] = useState("");
  const [result, setResult] = useState("");
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post('/check-salary', {salary: Number(salary),
      });
      setResult(response.data.message)
    } catch(error) {
      console.error(error)
      setResult("Unable to check the salary.")
      }
    }

  return (
    <main>
      <h1>Salary Checker</h1>
      <form onSubmit={handleSubmit}>
        <label htmlFor="salary"> Salary: </label>
        <input
        required
        id="salary"
        type="number"
        value={salary}
        onChange={(e) => setSalary(e.target.value)}
        placeholder="Enter your salary"
        />
        <button type="submit">Check Salary</button>
      </form>
      {result && <p>{result}</p>}
    </main>
  )
}

export default App;