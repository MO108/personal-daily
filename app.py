import random # 别忘了导入 random 模块
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_key'] = 'a_super_secret_key_that_is_hard_to_guess' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# (数据库模型部分保持不变，这里省略...)
class SuccessDiary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content1 = db.Column(db.Text, nullable=False)
    content2 = db.Column(db.Text, nullable=False)
    content3 = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class DailyInsight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# --- 首页路由 ---
@app.route('/')
def index():
    latest_diary = SuccessDiary.query.order_by(SuccessDiary.date_posted.desc()).first()
    latest_insight = DailyInsight.query.order_by(DailyInsight.date_posted.desc()).first()
    
    recruitments = [
        {'title': '公司招聘汇总', 'link': 'https://rvbrtqu27l.feishu.cn/base/RBelbeXBqaDE7IsrZ2FcZTYNnRA?table=tblS0HrPIah9ZKOu&view=vewh2m8QIt'},
        {'title': '公司招聘投递', 'link': 'https://pcn1sbp4j74a.feishu.cn/base/StuFbOoxyamdKbswW61cXNHDnsg'},
        {'title': '教师招聘投递', 'link': 'https://pcn1sbp4j74a.feishu.cn/base/SK6tbZiRZaZn1MsOIzacaUO2npe'}
    ]

    # --- 新增：励志名言池 ---
    quotes = [
        "Toda mi ambición es ser libre toda mi vida",
        "顺颂时宜，豫立亨通",
        "何时葡萄才熟透，你要静候再静候",
        "留在港口的小船最安全，但亲爱的，那不是造船的目的",
        "Some days you bloom，some days you grow roots. Both matter.",
        "给世界按最高价报价",
        "保护自己不被摧毁",
        "任何时候都不要粗暴的对待自己",
        "种一棵树最好的时间是十年前，其次是现在。",
        "今天也要元气满满哦！",
       
    ]
    random_quote = random.choice(quotes) # 随机选择一句
    
    return render_template('index.html', latest_diary=latest_diary, latest_insight=latest_insight, recruitments=recruitments, quote=random_quote)

# --- (其他路由函数保持不变，这里省略...) ---
@app.route('/add_diary', methods=['POST'])
def add_diary():
    if request.method == 'POST':
        content1 = request.form['content1']
        content2 = request.form['content2']
        content3 = request.form['content3']
        if content1 and content2 and content3:
            new_diary = SuccessDiary(content1=content1, content2=content2, content3=content3)
            db.session.add(new_diary)
            db.session.commit()
            flash('今日成功日记已记录！', 'success')
        else:
            flash('请填写全部三项成功事项哦。', 'error')
    return redirect(url_for('index'))

@app.route('/add_insight', methods=['POST'])
def add_insight():
    if request.method == 'POST':
        insight_content = request.form['insight_content']
        if insight_content:
            new_insight = DailyInsight(content=insight_content)
            db.session.add(new_insight)
            db.session.commit()
            flash('心得已成功记录！', 'success')
        else:
            flash('心得内容不能为空。', 'error')
    return redirect(url_for('index'))

# (这是你要添加的新函数)
@app.route('/summary')
def summary():
    # 查询所有的成功日记和每日心得，并按日期倒序排列
    all_diaries = SuccessDiary.query.order_by(SuccessDiary.date_posted.desc()).all()
    all_insights = DailyInsight.query.order_by(DailyInsight.date_posted.desc()).all()
    # 将查询结果发送给一个新的 summary.html 模板
    return render_template('summary.html', diaries=all_diaries, insights=all_insights)
# --- 启动部分 ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)