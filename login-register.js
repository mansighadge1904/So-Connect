const wrapper = document.querySelector('.wrapper');
const loginLink = document.querySelector('.login-link');
const registerLink = document.querySelector('.register-link');
// const loginBtn = document.querySelector('.login-btn');
// const registerBtn = document.querySelector('.register-btn');
// const homePage = document.querySelector('.home-page');


registerLink.addEventListener('click', ()=> {
    wrapper.classList.add('active');
});
loginLink.addEventListener('click', ()=> {
    wrapper.classList.remove('active');
});
// loginBtn.addEventListener('click', ()=>{
//     homePage.classList.add('present');
// });