<template>
  <div class="register_container">
    <div class="login_title">用户注册</div>
    <el-form ref="registerFormRef" :model="registerForm" :rules="registerFormRules" label-width="0px"
             class="login_form">
      <!-- 用户名 -->
      <el-form-item prop="username">
        <el-input v-model.trim="registerForm.username" prefix-icon="iconfont icon-gerenxinxi" placeholder="用户名"></el-input>
      </el-form-item>
      <!-- 密码 -->
      <el-form-item prop="password">
        <el-input v-model="registerForm.password" prefix-icon="iconfont icon-tianchongxing-" type="password"
                  placeholder="密码" show-password></el-input>
      </el-form-item>
      <!-- 真实姓名 -->
      <el-form-item prop="cardName">
        <el-input v-model="registerForm.cardName" prefix-icon="iconfont icon-ren" placeholder="真实姓名"></el-input>
      </el-form-item>
      <!-- 借阅证编号 -->
      <el-form-item prop="cardNumber">
        <el-input v-model.number="registerForm.cardNumber" prefix-icon="iconfont icon-card" placeholder="借阅证编号"
                  disabled></el-input>
      </el-form-item>
      <!-- 提交按钮 -->
      <el-form-item class="btns">
        <el-button type="primary" @click="submitRegister">提交注册</el-button>
        <el-button @click="$router.back()">返回</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      registerForm: {
        username: '',
        password: '',
        cardName: '',
        cardNumber: this.generateCardNumber(), // 自动生成
        ruleNumber: 1, // 默认规则编号
        status: 1, // 默认启用状态
      },
      registerFormRules: {
        username: [
          { required: true, message: '用户名不能为空', trigger: 'blur' },
          { min: 3, max: 20, message: '长度在3到20个字符', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '密码不能为空', trigger: 'blur' },
          { min: 6, max: 15, message: '长度在6到15个字符', trigger: 'blur' }
        ],
        cardName: [
          { required: true, message: '请输入真实姓名', trigger: 'blur' }
        ]
      }
    };
  },
  methods: {
    generateCardNumber() {
      const prefix = Math.floor(1000000000 + Math.random() * 9000000000);
      return prefix;
    },
    async submitRegister() {
      this.$refs.registerFormRef.validate(async valid => {
        if (!valid) return;

        const res = await this.$http.post('user/register', this.registerForm);

        if (res.data.status !== 200) {
          return this.$message.error(res.data.msg || '注册失败');
        }

        this.$message.success('注册成功');
        this.$router.push('/login');
      });
    }
  }
};
</script>

<style lang="less" scoped>
.register_container {
  background: url(http://img2.baidu.com/it/u=409978650,3642962641&fm=253&app=120&f=JPEG?w=1422&h=1200) no-repeat 0px 0px;
  background-size: cover;
  height: 120%;
  position: relative;
}

.login_form {
  width: 450px;
  margin: 100px auto;
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
</style>

