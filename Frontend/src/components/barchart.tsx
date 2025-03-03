import ReactEcharts from 'echarts-for-react';

function BarChart() {
    const option = {
        backgroundColor: '#F9F9FA',
        title: {
            text: 'Traffic by Device',
            left: '0%',
            top: '3%',
            textStyle: {
                fontWeight: 'bold',
                color: '#333',
                fontSize: 14
            }
        },
        xAxis: {
            type: 'category',
            data: ['Linux', 'Mac', 'iOS', 'Windows', 'Android', 'Other'],
            axisLine: {
                show: false
            },
            axisTick: {
                show: false
            },
            axisLabel: {
                fontSize: 11, // Smaller font size for x-axis labels
                interval: 0,   // Show all labels
                rotate: 0      // No rotation
            }
        },
        yAxis: {
            type: 'value',
            axisLabel: {
                formatter: function(value: any) {
                    if (value === 0) return '0';
                    return value / 1000 + 'K';
                }
            },
            splitLine: {
                show: false  // Remove the horizontal grid lines
            }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            top: '20%', // Increased to make room for title
            containLabel: true
        },
        series: [
            {
                data: [
                    {value: 17500, itemStyle: {color: '#d8f1f9'}}, // Linux
                    {value: 30000, itemStyle: {color: '#03045e'}}, // Mac
                    {value: 21000, itemStyle: {color: '#39a9c9'}}, // iOS
                    {value: 33000, itemStyle: {color: '#92bfff'}}, // Windows
                    {value: 13000, itemStyle: {color: '#cad6f1'}}, // Android
                    {value: 25000, itemStyle: {color: '#1a75a5'}}  // Other
                ],
                type: 'bar',
                barWidth: '50%', // Wider bars
                barGap: '10%',   // Less gap between bars
                itemStyle: {
                    borderRadius: [20, 20, 20, 20] // Rounded only at the top
                },
                showBackground: false
            }
        ],
        tooltip: {
            trigger: 'item',
            formatter: '{b}: {c}'
        }
    };
    
    return <ReactEcharts 
        option={option}
        style={{ height: '240px', width: '100%' }} 
    />;
}

export default BarChart;