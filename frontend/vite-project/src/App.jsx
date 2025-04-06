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
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setResult(null);

    try {
      const response = await axios.post("/api/predict", formData);
      setResult(response.data.result);
    } catch (err) {
      setError("无法完成预测，请检查后端是否正常运行！");
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center p-6">
      <h1 className="text-4xl font-bold mb-6">心血管疾病预测系统</h1>
      <form
        onSubmit={handleSubmit}
        className="grid grid-cols-2 gap-4 bg-white p-8 rounded-2xl shadow-md w-full max-w-3xl"
      >
        {Object.keys(formData).map((key) => (
          <div key={key} className="flex flex-col">
            <label className="text-sm font-medium mb-1 capitalize">{key.replace(/_/g, " ")}</label>
            <select
              name={key}
              value={formData[key]}
              onChange={handleChange}
              className="border rounded px-3 py-2"
            >
              {key === "age_group" &&
                ["young", "middle", "old"].map((v) => <option key={v}>{v}</option>)}
              {key === "bmi_group" &&
                ["underweight", "normal", "overweight", "obese"].map((v) => <option key={v}>{v}</option>)}
              {key === "ap_hi_group" &&
                ["normal", "high", "very_high"].map((v) => <option key={v}>{v}</option>)}
              {["cholesterol", "gluc"].includes(key) &&
                ["1", "2", "3"].map((v) => <option key={v}>{v}</option>)}
              {key === "smoke" &&
                ["0", "1"].map((v) => <option key={v}>{v}</option>)}
            </select>
          </div>
        ))}

        <div className="col-span-2 mt-4 text-center">
          <button
            type="submit"
            className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700"
          >
            立即诊断
          </button>
        </div>
      </form>

      {result && (
        <div className="mt-6 text-xl font-semibold text-green-700">{result}</div>
      )}

      {error && (
        <div className="mt-6 text-xl font-semibold text-red-600">{error}</div>
      )}
    </div>
  );
};

export default App;
