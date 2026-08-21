// パスワード表示
// 参考：https://itsakura.com/js-password

// テンプレートのチェックボックスを取得
const chk1 = document.getElementById('chk1');

// 入力されたパスワードを取得
const pass3 = document.querySelector('input[name="password"]');

// チェックボックスがクリックされたら、パスワードを表示する
chk1.addEventListener('click', function () {
    pass3.type = chk1.checked ? 'text' : 'password';
});