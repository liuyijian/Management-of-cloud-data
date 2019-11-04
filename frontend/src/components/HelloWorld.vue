<template>
  <div class="hello">
    <el-container>
      <el-header>
        <span style="font-size:28px; font-weight:bold;">以图搜书检索系统</span>
      </el-header>
      <el-main>
        <div>
          <el-upload
            class="upload-demo"
            drag
            :before-upload="beforeAvatarUpload"
            :on-success="handleAvatarSuccess"
            action="http://localhost:5000/">
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">将书籍封面图片拖到此处，或<em>点击上传</em></div>
            <div class="el-upload__tip" slot="tip">只能上传jpg/png文件，且不超过2MB</div>
          </el-upload>
        </div>
        <el-row v-if="show_buttons" style="margin-top:15px">
          <el-button type="primary" v-bind:plain="get_button_status(1)" v-on:click="on_click_button(1)">相同书名</el-button>
          <el-button type="success" v-bind:plain="get_button_status(2)" v-on:click="on_click_button(2)">相同作者</el-button>
          <el-button type="warning" v-bind:plain="get_button_status(3)" v-on:click="on_click_button(3)">相同出版社</el-button>
        </el-row>

        <div>
          <el-table
            ref="filterTable"
            :data="tableData"
            style="width: 100%"
            stripe
          >

            <el-table-column label="封面图片">
              <template slot-scope="scope">
<!--                <img :src="scope.row.img" width="80" height="80" class="head_pic"/>-->
                <img :src="scope.row.coverUrl" height="120" class="head_pic"/>
              </template>
            </el-table-column>

            <el-table-column prop="title" label="书名"></el-table-column>
            <el-table-column prop="author" label="作者"></el-table-column>
            <el-table-column prop="publisher" label="出版社"></el-table-column>
<!--            <el-table-column-->
<!--              prop="tag"-->
<!--              label="筛选条件"-->
<!--              :filters="[{ text: '相同出版社', value: '相同出版社' }, { text: '相同作者', value: '相同作者' }, { text: '相同书名', value: '相同书名' }]"-->
<!--              :filter-method="filterTag"-->
<!--              filter-placement="bottom-end">-->
<!--              <template slot-scope="scope">-->
<!--                <el-tag-->
<!--                  :type="selectTag(scope)"-->
<!--                  disable-transitions>{{scope.row.tag}}-->
<!--                </el-tag>-->
<!--              </template>-->
<!--            </el-table-column>-->
            <el-table-column prop="source" label="来源"></el-table-column>
          </el-table>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  data() {
    return {
      tableData: [],
      accurate_result: [],
      same_title_result: [],
      same_author_result: [],
      same_publisher_result: [],
      show_buttons: false,
      table_status: 0
    };
  },
  methods: {
    handleAvatarSuccess(res, file) {
      console.log(res);
      this.tableData = res.data[0];
      this.accurate_result = res.data[0];
      this.same_title_result = res.data[1];
      this.same_author_result = res.data[2];
      this.same_publisher_result = res.data[3];
      this.show_buttons = true;
    },
    beforeAvatarUpload(file) {
      const isJPG = file.type === 'image/jpeg';
      const isLt2M = file.size / 1024 / 1024 < 2;

      if (!isJPG) {
        this.$message.error('上传图片只能是 JPG 格式!');
      }
      if (!isLt2M) {
        this.$message.error('上传图片大小不能超过 2MB!');
      }
      return isJPG && isLt2M;
    },
    formatter(row, column) {
      return row.address;
    },
    filterTag(value, row) {
      return row.tag === value;
    },
    filterHandler(value, row, column) {
      const property = column['property'];
      return row[property] === value;
    },
    selectTag(scope) {
      if (scope.row.tag === '相同书名') return 'primary';
      if (scope.row.tag === '相同作者') return 'success';
      if (scope.row.tag === '相同出版社') return 'warning';
    },
    get_button_status(button_id) {
      switch (button_id) {
        case 1:
          return this.table_status !== 1;
        case  2:
          return this.table_status !== 2;
        case 3:
          return this.table_status !== 3;
      }
    },
    on_click_button(button_id) {
        switch (button_id) {
        case 1:
          if (this.table_status === 1)
          {
            this.table_status = 0;
            this.tableData = this.accurate_result;
          }
          else
          {
            this.table_status = 1;
            this.tableData = this.same_title_result;
          }
          break;
        case  2:
          if (this.table_status === 2)
          {
            this.table_status = 0;
            this.tableData = this.accurate_result;
          }
          else
          {
            this.table_status = 2;
            this.tableData = this.same_author_result;
          }
          break;
        case 3:
          if (this.table_status === 3)
          {
            this.table_status = 0;
            this.tableData = this.accurate_result;
          }
          else
          {
            this.table_status = 3;
            this.tableData = this.same_publisher_result;
          }
          break;
      }
    },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
.el-header {
    background-color: #EBEEF5;
    color: #333;
    text-align: center;
    line-height: 60px;
  }
.el-main {
  text-align: center;
}
.demo-table-expand {
    font-size: 0;
  }
.demo-table-expand label {
  width: 90px;
  color: #99a9bf;
}
.demo-table-expand .el-form-item {
  margin-right: 0;
  margin-bottom: 0;
  width: 50%;
}
</style>
