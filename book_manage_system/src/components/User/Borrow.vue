<template>
  <div class="search_container">
    <!-- 面包屑导航区域 -->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item>首页</el-breadcrumb-item>
      <el-breadcrumb-item>借阅信息</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card shadow="always">
      <!-- 搜索内容和导出区域 -->
      <el-row>
        <el-col :span="6"
          >条件搜索:<el-select
            v-model="queryInfo.condition"
            filterable
            placeholder="请选择"
            style="margin-left: 15px"
          >
            <el-option
              v-for="item in options"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            >
            </el-option>
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-input
            placeholder="请输入内容"
            v-model="queryInfo.query"
            class="input-with-select"
            @keyup.enter.native="searchBookBorrowByPage"
          >
            <el-button
              slot="append"
              icon="el-icon-search"
              @click="searchBookBorrowByPage"
            ></el-button> </el-input
        ></el-col>
        <el-col :span="2" style="float: right">
          <download-excel
            class="export-excel-wrapper"
            :data="tableData"
            :fields="json_fields"
            :header="title"
            name="图书借阅表格.xls"
          >
            <!-- 上面可以自定义自己的样式，还可以引用其他组件button -->
            <el-button type="primary" class="el-icon-printer" size="mini"
              >导出Excel</el-button
            >
          </download-excel>
        </el-col>
        <el-col :span="2" style="float: right">
          <el-button
            type="primary"
            class="el-icon-printer"
            size="mini"
            @click="downLoad"
            >导出PDF</el-button
          >
        </el-col>
        <el-col :span="2" style="float: right">
         
         <el-button type="success" class="el-icon-full-screen" size="mini" @click="fullScreen"
           >全屏</el-button
         >
       </el-col>
      </el-row>
      <!-- 表格区域 -->
      <el-table
        :data="tableData"
        border
        style="width: 100%"
        stripe
        id="pdfDom"
        :default-sort="{ prop: 'cardNumber', order: 'ascending' }"
        v-loading="loading"
        element-loading-text="拼命加载中"
        element-loading-spinner="el-icon-loading"
        element-loading-background="rgba(0, 0, 0, 0.8)"
      >
        <el-table-column prop="cardNumber" label="借阅编号" sortable>
        </el-table-column>
        <el-table-column prop="bookNumber" label="图书编号" sortable>
        </el-table-column>
        <el-table-column prop="borrowDate" label="借阅日期" sortable>
        </el-table-column>
        <el-table-column prop="closeDate" label="截止日期" sortable>
        </el-table-column>
        <el-table-column prop="returnDate" label="归还日期" sortable>
        </el-table-column>
        <el-table-column label="操作" width="150px">
          <template slot-scope="scope">
            <el-button size="mini" type="success" @click="openRateDialog(scope.row)">点评</el-button>
          </template>
        </el-table-column>

      </el-table>
      <!-- 分页查询区域 -->
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="this.queryInfo.pageNum"
        :page-sizes="[1, 2, 3, 4, 5]"
        :page-size="this.queryInfo.pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="this.total"
      >
      </el-pagination>
    </el-card>

    <!-- 评分弹窗 -->
    <el-dialog title="给图书评分" :visible.sync="rateVisible" width="30%">
      <el-form label-position="right" label-width="100px">
        <el-form-item label="评分（0-10）">
          <el-input v-model="rating" :min="0" :max="10" :step="1"></el-input>
        </el-form-item>
        <el-button type="primary" @click="submitRating">提交评分</el-button>
      </el-form>
    </el-dialog>

  </div>
</template>

<script>
export default {
  data() {
    return {
      options: [
        {
          value: "book_number",
          label: "图书编号",
        },
        {
          value: "borrow_date",
          label: "借阅日期",
        },
        {
          value: "close_date",
          label: "截止日期",
        },
        {
          value: "return_date",
          label: "归还日期",
        },
      ],
      tableData: [
        {
          cardNumber: Number,
          bookNumber: Number,
          borrowId: Number,
          borrowDate: "",
          closeDate: "",
          returnDate: "",
          createTime: "",
          updateTime: "",
        },
      ],
      queryInfo: {
        pageNum: 1,
        pageSize: 5,
        condition: "",
        query: "",
        cardNumber: window.sessionStorage.getItem("cardNumber"),
      },
      total: 0,
      title: "图书借阅表格",
      json_fields: {
        借阅编号: "cardNumber",
        图书编号: "bookNumber",
        借阅日期: "borrowDate",
        截止日期: "closeDate",
        归还日期: "returnDate",
      },
      loading: true,

      rateVisible: false,
      rating: 0,
      currentBookNumber: null,
    };
  },
  methods: {

    // 打开评分弹窗
    openRateDialog(row) {
      this.currentBookNumber = row.bookNumber;
      this.rating = 0;
      this.rateVisible = true;
    },

    // 提交评分
    async submitRating() {
      if (this.rating < 0 || this.rating > 10) {
        this.$message.warning("评分必须在 0 到 10 分之间");
        return;
      }

      const ratingData = {
        bookNumber: this.currentBookNumber,
        score: this.rating
      };

      const { data: res } = await this.$http.post("/user/rate_book", ratingData);
      if (res.status !== 200) {
        return this.$message.error(res.msg);
      }

      this.$message.success(res.msg);
      this.rateVisible = false;
    },

    handleSizeChange(val) {
      this.queryInfo.pageSize = val;

      this.searchBookBorrowByPage();
    },
    handleCurrentChange(val) {
      this.queryInfo.pageNum = val;

      this.searchBookBorrowByPage();
    },
    async searchBookBorrowByPage() {
      this.loading = true;
      const { data: res } = await this.$http.post(
        "user/get_bookborrow",
        this.queryInfo
      );

      this.tableData = [];
      // console.log(res);
      if (res.status !== 200) {
        this.total = 0;
        this.loading = false;
        return this.$message.error(res.msg);
      }
      this.$message.success({
        message: res.msg,
        duration: 1000,
      });
      this.tableData = res.data.records;
       this.total = parseInt(res.data.total);
      this.loading = false;
    },
    downLoad() {
      this.getPdf(this.title); //参数是下载的pdf文件名
    },
    fullScreen(){
          // Dom对象的一个属性: 可以用来判断当前是否为全屏模式(trueORfalse)
    let full = document.fullscreenElement;
    // 切换为全屏模式
    if(!full){
        // 文档根节点的方法requestFullscreen实现全屏模式
        document.documentElement.requestFullscreen();
    }else{
        // 退出全屏模式
        document.exitFullscreen();
    }
    }
  },
  created() {
    this.searchBookBorrowByPage();
  },
};
</script>

<style>
</style>