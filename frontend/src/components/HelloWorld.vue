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
        <div>
          <el-table
            ref="filterTable"
            :data="tableData"
            style="width: 100%"
            stripe
          >
            <el-table-column type="expand">
              <template slot-scope="props">
                <el-form label-position="left" inline class="demo-table-expand">
                  <el-form-item label="书名">
                    <span>{{ props.row.name }}</span>
                  </el-form-item>
                  <el-form-item label="作者">
                    <span>{{ props.row.author }}</span>
                  </el-form-item>
                  <el-form-item label="出版社">
                    <span>{{ props.row.address }}</span>
                  </el-form-item>
                  <el-form-item label="简介">
                    <span>{{ props.row.description }}</span>
                  </el-form-item>
                </el-form>
              </template>
            </el-table-column>

            <el-table-column label="封面图片">
            　　<template slot-scope="scope">
            　　　　<img :src="scope.row.img" width="80" height="80" class="head_pic"/>
            　　</template>
            </el-table-column>

            <el-table-column prop="name" label="书名"></el-table-column>
            <el-table-column prop="author" label="作者"></el-table-column>
            <el-table-column prop="address" label="出版社" :formatter="formatter"></el-table-column>
            <el-table-column
              prop="tag"
              label="筛选条件"
              :filters="[{ text: '相同出版社', value: '相同出版社' }, { text: '相同作者', value: '相同作者' }, { text: '相同书名', value: '相同书名' }]"
              :filter-method="filterTag"
              filter-placement="bottom-end">
              <template slot-scope="scope">
                <el-tag
                  :type="selectTag(scope)"
                  disable-transitions>{{scope.row.tag}}
                </el-tag>
              </template>
            </el-table-column>
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
      tableData: []
    };
  },
  methods: {
    handleAvatarSuccess(res, file) {
      console.log(res)
      this.tableData = res.tableData
    },
    beforeAvatarUpload(file) {
      const isJPG = file.type === 'image/jpeg';
      const isLt2M = file.size / 1024 / 1024 < 2;

      if (!isJPG) {
        this.$message.error('上传头像图片只能是 JPG 格式!');
      }
      if (!isLt2M) {
        this.$message.error('上传头像图片大小不能超过 2MB!');
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
    }
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
