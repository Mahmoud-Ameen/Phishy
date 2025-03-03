import ReactEcharts from 'echarts-for-react';

const PieChart = () => {
    const option = {
        backgroundColor: '#F9F9FA',
        title: {
          text: 'Traffic by Location',
          left: '5%',
          top: '3%',
          textStyle: {
            fontWeight: 'bold',
            color: '#333',
            fontSize: 14
          }
        },
        color: ['#00B4D8', '#0077B6', '#03045E', '#90E0EF'],
        tooltip: {
          trigger: 'item',
          formatter: '{b}: {c}%'
        },
        legend: {
          orient: 'vertical',
          right: '13%',
          top: 'center',
          itemGap: 10,
          icon: 'circle',
          formatter: function(name:any) {
            return [
              `${name}`,
            ].join('  ');
          },
          textStyle: {
            rich: {
              value: {
                fontWeight: 'normal',
                width: 60,
                align: 'right'
              },
              marker: {
                fontSize: 10
              }
            },
            fontSize: 10
          }
        },
        series: [
          {
            name: 'Traffic by Location',
            type: 'pie',
            radius: ['30%', '60%'],
            center: ['30%', '55%'],
            padAngle:8,
            avoidLabelOverlap: false,
            itemStyle: {
              borderWidth: 0,
              borderRadius: 10
            },
            label: {
              show: false
            },
            labelLine: {
              show: false
            },
            emphasis: {
              scale: true,
              scaleSize: 10
            },
            data: [
              { value: 52.1, name: 'United States' },
              { value: 22.8, name: 'Canada' },
              { value: 13.9, name: 'Mexico' },
              { value: 11.2, name: 'Egypt' }
            ]
          }
        ]
      };

    return (
        <ReactEcharts
            option={option}
            style={{ height: '240px', width: '100%'}}
        />
    );
};

export default PieChart;