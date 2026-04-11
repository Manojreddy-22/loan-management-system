import { useState } from "react";
import axios from "axios";

function App() {
  const [form, setForm] = useState({
    name: "",
    age: "",
    income: "",
    loan_amount: "",
    interest_rate: "",
    tenure: "",
    loan_type: "",
    application_date: "",
    credit_score: ""
  });

  const [result, setResult] = useState(null);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async () => {
    try {
      const res = await axios.post("http://127.0.0.1:8000/loan", {
        name: form.name,
        age: Number(form.age),
        income: Number(form.income),
        loan_amount: Number(form.loan_amount),
        interest_rate: Number(form.interest_rate),
        tenure: Number(form.tenure),
        loan_type: form.loan_type,
        application_date: form.application_date,
        credit_score: form.credit_score ? Number(form.credit_score) : null
      });

      setResult(res.data);
    } catch (error) {
      console.log(error);
      alert("Backend not connected ❌");
    }
  };

  return (
    <div style={{ padding: "30px" }}>
      <h1>🏦 Loan Management System</h1>

      <input name="name" placeholder="Name" onChange={handleChange} /><br/><br/>
      <input name="age" placeholder="Age" onChange={handleChange} /><br/><br/>
      <input name="income" placeholder="Income" onChange={handleChange} /><br/><br/>
      <input name="loan_amount" placeholder="Loan Amount" onChange={handleChange} /><br/><br/>

      <input name="interest_rate" placeholder="Interest Rate (%)" onChange={handleChange} /><br/><br/>
      <input name="tenure" placeholder="Tenure (months)" onChange={handleChange} /><br/><br/>

      <input name="loan_type" placeholder="Loan Type (Home/Personal)" onChange={handleChange} /><br/><br/>

      <input type="date" name="application_date" onChange={handleChange} /><br/><br/>

      <input name="credit_score" placeholder="Credit Score (optional)" onChange={handleChange} /><br/><br/>

      <button onClick={handleSubmit}>Check Loan</button>

      {result && (
        <div style={{ marginTop: "20px" }}>
          <h2>Result</h2>
          <p>Name: {result.name}</p>
          <p>Loan Type: {result.loan_type}</p>
          <p>EMI: ₹{result.emi}</p>
          <p>Status: {result.status}</p>
        </div>
      )}
    </div>
  );
}

export default App;