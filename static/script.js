// 模擬 IoT 數據更新
        function updateSensorData() {
            const tempElement = document.getElementById('temperature');
            const humidityElement = document.getElementById('humidity');

            // 隨機生成新的溫度和濕度數據
            const newTemp = (Math.random() * 5 + 20).toFixed(1); // 20.0 - 25.0
            const newHumidity = (Math.random() * 20 + 50).toFixed(0); // 50 - 70

            tempElement.textContent = `${newTemp}°C`;
            humidityElement.textContent = `${newHumidity}%`;
        }

        // 每 5 秒更新一次數據
        setInterval(updateSensorData, 5000);

        // 設備開關控制
        function setupDeviceToggle(buttonId, statusId, deviceName) {
            const button = document.getElementById(buttonId);
            const statusElement = document.getElementById(statusId);
            let isOn = false;

            button.addEventListener('click', () => {
                isOn = !isOn;
                if (isOn) {
                    button.textContent = '關閉';
                    button.classList.remove('off');
                    statusElement.textContent = '開啟';
                    console.log(`${deviceName} 已開啟`);
                } else {
                    button.textContent = '開啟';
                    button.classList.add('off');
                    statusElement.textContent = '關閉';
                    console.log(`${deviceName} 已關閉`);
                }
            });
        }

        setupDeviceToggle('light-toggle-btn', 'light-status', '客廳燈');
        setupDeviceToggle('fan-toggle-btn', 'fan-status', '風扇');

        // 初始數據載入
        document.addEventListener('DOMContentLoaded', () => {
            updateSensorData();
        });