<template>
  <div class="main">
    <div class="gather">
      <el-row :gutter="15">
        <el-col :span="12">
          <el-card class="box-card">
            <h1 class="total">粉丝总数：{{fans.total}}</h1>
            <p class="detailed">男性：{{fans.man}}</p>
            <p class="detailed">女性：{{fans.woman}}</p>
            <p class="detailed">其他：{{fans.other}}</p>
            <div class="bar_report" ref="fans"></div>
          </el-card>
        </el-col>
        <el-col :span="12">
          <el-card class="box-card">
            <h1 class="total">优惠券总数：{{discount.total}}</h1>
            <p class="detailed">已使用：{{discount.use}}</p>
            <p class="detailed">未使用：{{discount.un_use}}</p>
            <div class="bar_report" ref="discount"></div>
          </el-card>
        </el-col>
      </el-row>
    </div>
    <div class="ranking">
      <el-card class="box-card">
        <div class="chart_report" ref="experience"></div>
      </el-card>
    </div>
    <div class="ranking">
      <el-card class="box-card">
        <div class="chart_report" ref="score"></div>
      </el-card>
    </div>
  </div>
</template>

<script>
  export default {
    name: "main",
    data () {
      return {
        fans: {},
        discount: {},
        experience: [],
        score: []
      }
    },
    created () {
      this.getData();
    },
    methods: {
      getData () {
        this.$axios.post('/api/admin/report')
          .then((res) => {
            this.fans = res.data.fans;
            this.discount = res.data.discount;
            this.experience = res.data.experience;
            this.score = res.data.score;
            this.$nextTick(() => {
              this.drawPie(this.$refs.fans, 'fans');
              this.drawPie(this.$refs.discount, 'discount');
              this.drawChart(this.$refs.experience, '经验排行榜');
              this.drawChart(this.$refs.score, '积分排行榜');
            });
          })
          .catch((err) => {
            console.log(err);
          })
      },
      drawPie (ele, type = 'fans') {
        let data = [];
        if (type == 'fans') {
          data = [
            {value: this.fans.man, name: '男'},
            {value: this.fans.woman, name: '女'},
            {value: this.fans.other, name: '其他'}
          ]
        } else if (type == 'discount') {
          data = [
            {value: this.discount.use, name: '已使用'},
            {value: this.discount.un_use, name: '未使用'}
          ]
        }
        let echarts = this.$echarts.init(ele);
        let option = {
          tooltip: {
            trigger: 'item',
            formatter: "数量：{c} ({d}%)"
          },
          calculable: true,
          series: [
            {
              type: 'pie',
              radius: '75%',
              center: ['50%', '50%'],
              label: {
                normal: {
                  show: true,
                  position: 'inner'
                }
              },
              data: data
            }
          ]
        }
        echarts.setOption(option);
      },
      drawChart (ele, title = '经验排行榜', type = 'experience') {
        let xData = [], yData = [];
        if (type == 'experience') {
          this.experience.map((ex) => {
            xData.push(ex.username);
          });
          this.experience.map((ex) => {
            yData.push(ex.experience);
          });
        } else if (type == 'discount') {
          this.score.map((ex) => {
            xData.push(ex.username);
          });
          this.score.map((ex) => {
            yData.push(ex.score);
          });
        }
        let echarts = this.$echarts.init(ele);
        let option = {
          title: {
            text: title,
          },
          tooltip: {
            trigger: 'axis'
          },
          calculable: true,
          xAxis: [
            {
              type: 'category',
              data: xData,
              axisLabel: {
                interval: 0,
                rotate: 45,
                formatter: function (value) {
                  return value.length > 5 ? value.substring(0, 5) + '...' : value;
                }
              }
            }
          ],
          yAxis: [
            {
              type: 'value'
            }
          ],
          series: [
            {
              type: 'bar',
              label: {
                normal: {
                  show: true,
                  position: 'top'
                }
              },
              data: yData
            }
          ]
        }
        echarts.setOption(option);
      }
    }
  }
</script>

<style scoped>
  .main {
    padding: 12px;
  }

  .total {
    font-size: 18px;
    font-weight: normal;
  }

  .detailed {
    display: inline-block;
    font-size: 14px;
    padding-top: 15px;
    padding-right: 15px;
  }

  .bar_report {
    margin: 20px auto 0;
    width: 200px;
    height: 200px;
  }

  .ranking {
    margin-top: 12px;
  }

  .chart_report {
    height: 300px;
  }
</style>
