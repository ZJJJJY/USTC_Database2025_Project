<template>
  <div class="comment_container">
    <div class="backgroundImg">
      <img src="https://img0.baidu.com/it/u=135509537,3428620485&fm=253&fmt=auto&app=138&f=JPEG?w=380&h=686" alt="" />
    </div>

    <div class="barrages-drop">
      <!-- 主评论输入框 -->
      <div class="addMain">
        <el-input v-model.trim="input" placeholder="发表你的看法..." @keyup.enter.native="addContent">
          <el-button slot="append" icon="el-icon-edit" @click="addContent"></el-button>
        </el-input>
      </div>

      <!-- 评论列表 -->
      <div class="comment-list">
        <ul>
          <li v-for="(item, index) in barrageList" :key="index" class="comment-item">
            <div class="comment-header">
              <span class="username">{{ item.userName }}：</span>
            </div>
            <div class="comment-content">{{ item.msg }}</div>
            <div class="reply-btn" @click="openReplyBox(item.id)">回复</div>

            <!-- 子评论 -->
            <ul v-if="item.replies && item.replies.length > 0" class="replies">
              <li v-for="(reply, idx) in item.replies" :key="idx" class="reply-item">
                <div class="reply-header">
                  <span class="username">{{ reply.userName }}@{{item.userName}}</span>
                </div>
                <div class="reply-content">{{ reply.commentMessage }}</div>
              </li>
            </ul>
          </li>
        </ul>
      </div>

      <!-- 回复弹窗 -->
      <el-dialog title="回复评论" :visible.sync="replyVisible" width="40%">
        <el-input ref="replyInput" v-model.trim="replyInput" placeholder="输入你的回复..." @keyup.enter.native="submitReply">
          <el-button slot="append" icon="el-icon-edit" @click="submitReply"></el-button>
        </el-input>
      </el-dialog>
    </div>
  </div>


</template>



<script>
import { MESSAGE_TYPE } from "vue-baberrage";
import { nanoid, random } from "nanoid";
export default {
  data() {
    return {
      input: "",
      //弹幕列表，格式为数组
      barrageList: [],
      barrage: {
        id: "",
        avatar:
          "https://img0.baidu.com/it/u=825023390,3429989944&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=500",
        msg: "",
        time: "",
        type: MESSAGE_TYPE.NORMAL,
        barrageStyle: "",
        replies: [], // 子评论列表
      },

      // 弹窗相关字段
      replyVisible: false,
      replyInput: "",
      replyCommentId: null
    };
  },
  methods: {
      async addContent() {
        if (this.input.trim() === '' || /^\d+$/.test(this.input) || /^[a-zA-Z]+$/.test(this.input)) {
          this.$message.info("请不要输入无意义的内容");
          return;
        }

        const token = localStorage.getItem('token');
        const username = this.getUsernameFromToken(token);

        this.barrage.msg = this.input;
        this.barrage.userName = username;

        const { data: res } = await this.$http.post('user/add_comment', this.barrage);
        if (res.status !== 200) {
          return this.$message.error(res.msg);
        }

        this.getCommentList();
        this.input = "";
        this.$message.success(res.msg);
      },

      openReplyBox(commentId) {
        this.replyCommentId = commentId;
        this.replyVisible = true;
        this.$nextTick(() => {
          this.$refs.replyInput.focus(); // 自动聚焦输入框
        });
      },

      async submitReply() {
        if (this.replyInput.trim() === '' || /^\d+$/.test(this.replyInput) || /^[a-zA-Z]+$/.test(this.replyInput)) {
          this.$message.info("请不要输入无意义的内容");
          return;
        }


        const reply = {
          parentId: this.replyCommentId,
          msg: this.replyInput,
        };

        const { data: res } = await this.$http.post(`user/reply_comment`, reply);
        if (res.status !== 200) {
          return this.$message.error(res.msg);
        }

        this.replyInput = "";
        this.replyVisible = false;
        this.$message.success("回复成功！");

        this.getCommentList();
      },


    async getCommentList() {
      // 发送axios请求
      const { data: res } = await this.$http.get("user/get_commentlist");
      // console.log(res);
      if (res.status !== 200) {
        return this.$message.error(res.msg);
      }
      this.$message.success(res.msg);
      this.barrageList = res.data
      //添加空对象，数组更新，组件更新
      this.barrageList.push({})
    },

  },

  mounted(){
    this.getCommentList();
  }
};
</script>

<style lang="less" scoped>

.comment_container {
  position: relative;
  height: 100%;
  width: 100%;
}
.backgroundImg {
  position: absolute;
  height: 100%;
  width: 100%;
  img {
    height: 100%;
    width: 100%;
    opacity: 0.5;
  }
}
.barrages-drop {
  position: relative;
}





.barrages-drop {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start; // 垂直顶部对齐
  height: 100%;
  padding-bottom: 40px; // 给输入框留出底部空间
}

.comment-list {
  position: absolute;
  top: 100px;
  left: 50%;
  transform: translateX(-50%);
  width: 80%;
  max-height: 600px;
  overflow-y: auto;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  padding: 20px;
  margin-bottom: 20px;
}

.comment-list li {
  padding: 12px 16px;
  margin-bottom: 8px;
  border-radius: 8px;
  background-color: #f9f9f9;
  transition: background-color 0.3s ease;
  font-size: 14px;
  -webkit-font-smoothing: antialiased;
  font-family: "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;

  &:hover {
    background-color: #f1f1f1;
  }

  &:last-child {
    margin-bottom: 0;
  }
}


.addMain {
  width: 400px;
  background-color: #ffffffdd;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  padding: 15px 20px;

  .el-input__inner {
    border-radius: 8px;
    border: 1px solid #ddd;
    padding-right: 45px;
  }

  .el-button {
    background-color: #409EFF;
    color: white;
    border-radius: 8px;

    &:hover {
      background-color: #337ecc;
    }
  }
}

.reply-btn {
  cursor: pointer;
  color: #409EFF; // 蓝色
  font-size: 14px;
  margin-top: 8px;
  text-decoration: none;

  &:hover {
    color: #337ecc; // 深一点的蓝色
  }

  &:active {
    color: #2b6cbf; // 按下时的颜色
  }
}


</style>
