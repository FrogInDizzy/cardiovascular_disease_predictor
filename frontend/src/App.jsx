import React, { useState } from "react";
import axios from "axios";

const App = () => {
  const [formData, setFormData] = useState({
    age_group: "middle",
    bmi_group: "normal",
    ap_hi_group: "normal",
    cholesterol: "1",
    gluc: "1",
    smoke: "0",
  });

  const [result, setResult] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await axios.post("http://localhost:5000/api/predict", formData);
    setResult(response.data.result);
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-4">
      <h1 className="text-3xl font-bold mb-4">心血管疾病预测系统</h1>
      <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-4 bg-white p-6 rounded-xl shadow-md">
        {Object.keys(formData).map((key) => (
          <div key={key}>
            <label className="block text-sm font-semibold capitalize mb-1">{key.replace("_", " ")}</label>
            <select
              name={key}
              value={formData[key]}
              onChange={handleChange}
              className="border border-gray-300 rounded p-2 w-full"
            >
              {key === "age_group" && ["young", "middle", "old"].map((v) => <option key={v}>{v}</option>)}
              {key === "bmi_group" && ["underweight", "normal", "overweight", "obese"].map((v) => <option key={v}>{v}</option>)}
              {key === "ap_hi_group" && ["normal", "high", "very_high"].map((v) => <option key={v}>{v}</option>)}
              {key === "cholesterol" && ["1", "2", "3"].map((v) => <option key={v}>{v}</option>)}
              {key === "gluc" && ["1", "2", "3"].map((v) => <option key={v}>{v}</option>)}
              {key === "smoke" && ["0", "1"].map((v) => <option key={v}>{v}</option>)}
            </select>
          </div>
        ))}
        <div className="col-span-2 text-center">
          <button type="submit" className="bg-blue-600 text-white py-2 px-6 rounded hover:bg-blue-700">
            立即诊断
          </button>
        </div>
      </form>
      {result && <div className="mt-6 text-xl font-semibold text-green-700">{result}</div>}
    </div>
  );
};

export default App;
