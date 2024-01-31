document.addEventListener('DOMContentLoaded', function () {
    const startButton = document.getElementById('startButton');
    const scannedResults = document.getElementById('scannedResults');
    let scanning = false;

    startButton.addEventListener('click', function () {
        if (scanning) {
            Quagga.stop();
            startButton.textContent = 'Iniciar Escaneo';
        } else {
            Quagga.init({
                inputStream: {
                    type: 'LiveStream',
                    target: document.querySelector('#preview'),
                    constraints: {
                        facingMode: 'environment'
                    }
                },
                decoder: {
                    readers: ['ean_reader', 'ean_8_reader', 'code_39_reader', 'code_39_vin_reader', 'codabar_reader', 'upc_reader', 'upc_e_reader', 'i2of5_reader']
                }
            }, function (err) {
                if (err) {
                    console.error(err);
                    alert("Error al iniciar Quagga: " + err);
                    return;
                }
                console.log('Quagga initialized successfully');
                Quagga.start();
                console.log('Quagga started');
                startButton.textContent = 'Detener Escaneo';
            });
        }
        scanning = !scanning;
    });
    
    Quagga.onDetected(function (data) {
        console.log('Barcode detected:', data.codeResult.code);
        let code = data.codeResult.code;
        if (scannedResults.querySelector(`li[data-code="${code}"]`)) {
            console.log('Barcode already scanned');
            return;
        }
        let li = document.createElement('li');
        li.textContent = code;
        li.setAttribute('data-code', code);
        scannedResults.appendChild(li);
        console.log('Barcode added to list:', code);
    });
});