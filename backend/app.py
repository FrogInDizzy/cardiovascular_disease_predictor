from flask import Flask, request, jsonify
from flask_cors import CORS
from bn_engine import BayesianNetwork

app = Flask(__name__)
CORS(app)  # 允许前端跨域请求

# 加载 .bn 文件
bn = BayesianNetwork()
bn.load_from_file("heart_disease.bn")

@app.route("/api/predict", methods=["POST"])
def predict():
    data = request.get_json()

    evidence = {
        "age_group": data.get("age_group"),
        "bmi_group": data.get("bmi_group"),
        "ap_hi_group": data.get("ap_hi_group"),
        "cholesterol": data.get("cholesterol"),
        "gluc": data.get("gluc"),
        "smoke": data.get("smoke")
    }

    result_probs = bn.exact_inference("cardio", evidence)
    labels = bn.variables["cardio"].values

    # 找出最大概率的那个标签
    predicted = labels[result_probs.index(max(result_probs))]
    prob_percent = round(max(result_probs) * 100, 2)

    return jsonify({
        "result": f"预测结果：{'患病' if predicted == '1' else '未患病'}（概率 {prob_percent}%）",
        "raw": dict(zip(labels, result_probs))
    })

if __name__ == "__main__":
    app.run(debug=True)
