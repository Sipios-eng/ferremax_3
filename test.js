import http from 'k6/http';
import { sleep, check } from 'k6';

export let options = {
  vus: 10, // usuarios virtuales
  duration: '30s', // duración de la prueba
};

export default function () {
  let res = http.get('http://127.0.0.1:8000/');
  check(res, {
    'status es 200': (r) => r.status === 200,
  });
  sleep(1);
}
