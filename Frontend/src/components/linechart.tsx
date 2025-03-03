import ReactEcharts from 'echarts-for-react';

type EChartsParam = {
  name: string;
  seriesName: string;
  value: number;
  color: string;
}

function MyChartComponent() {
  const chartOptions = {
    backgroundColor: '#F9F9FA',
    color: ['#4F81BD', '#C5D9F1'],
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
      axisLine: {
        show: false
      },
      axisTick: {
        show: false
      },
      axisLabel: {
        color: '#999',
        fontSize: 12
      }
    },
    yAxis: {
      type: 'value',
      min: 0,
      max: 30000,
      interval: 10000,
      axisLine: {
        show: false
      },
      axisTick: {
        show: false
      },
      axisLabel: {
        formatter: function(value: number) {
          if (value === 0) return '0';
          return value.toLocaleString();
        },
        color: '#999',
        fontSize: 12
      },
      splitLine: {
        lineStyle: {
          type: 'dashed',
          color: '#eee'
        }
      }
    },
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(255, 255, 255, 0.9)',
      borderColor: '#ccc',
      borderWidth: 1,
      textStyle: {
        color: '#333'
      },
      formatter: function(params: EChartsParam[]) {
        let result = params[0].name + '<br/>';
        params.forEach(param => {
          result += `<span style="display:inline-block;margin-right:5px;border-radius:50%;width:10px;height:10px;background-color:${param.color};"></span> `;
          result += `${param.seriesName}: ${param.value.toLocaleString()}<br/>`;
        });
        return result;
      }
    },
    series: [
      {
        name: 'This week',
        type: 'line',
        smooth: true,
        symbol: 'none',
        lineStyle: {
          width: 2.5
        },
        data: [12000, 14000, 6000, 8000, 11000, 16000, 24000],
        areaStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [{
              offset: 0, color: 'rgba(79, 129, 189, 0.3)'
            }, {
              offset: 1, color: 'rgba(79, 129, 189, 0)'
            }]
          }
        }
      },
      {
        name: 'Last week',
        type: 'line',
        smooth: true,
        symbol: 'none',
        lineStyle: {
          width: 2.5,
          type: 'dotted'
        },
        data: [5000, 14000, 13000, 12000, 21000, 15000, 6000]
      }
    ],
    title: [
      {
        text: 'Total Users',
        left: '0%',
        top: '3%',
        textStyle: {
          fontWeight: 'bold',
          color: '#333',
          fontSize: 14
        }
      },
      {
        text: 'Total Opened Emails  ',
        left: '15%',
        top: '3%',
        textStyle: {
          fontWeight: 'normal',
          color: '#999',
          fontSize: 14
        }
      },
      {
        text: 'Operating Status',
        left: '35%',
        top: '3%',
        textStyle: {
          fontWeight: 'normal',
          color: '#999',
          fontSize: 14
        }
      },   
      {
        text: '|',
        left: '52%',
        top: '2%',
        textStyle: {
          fontWeight: 'bold',
          color: '#999',
          fontSize: 20
        }
      },
      {
        text: '●',
        left: '55%',
        top: '3%',
        textStyle: {
          fontWeight: 'normal',
          color: '#4F81BD',
          fontSize: 14
        }
      },
      {
        text: 'This week',
        left: '56.5%',
        top: '3%',
        textStyle: {
          fontWeight: 'bold',
          color: '#000',
          fontSize: 14
        }
      },
      {
        text: '●',
        left: '68%',
        top: '3%',
        textStyle: {
          fontWeight: 'normal',
          color: '#C5D9F1',
          fontSize: 14
        }
      },
      {
        text: 'Last week',
        left: '69.5%',
        top: '3%',
        textStyle: {
          fontWeight: 'bold',
          color: '#000',
          fontSize: 14
        }
      },
    ]
  };

  return (
    <div>
      <ReactEcharts option={chartOptions} />
    </div>
  );
}

export default MyChartComponent;