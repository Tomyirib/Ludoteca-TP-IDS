document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll('.form input, .form textarea').forEach(function (input) {
    input.addEventListener('keyup', handleEvent);
    input.addEventListener('blur', handleEvent);
    input.addEventListener('focus', handleEvent);
  });

  function handleEvent(e) {
    var input = e.target;
    var label = input.closest('.field-wrap').querySelector('label');

    if (!label) return;

    if (e.type === 'keyup') {
      if (input.value === '') {
        label.classList.remove('active', 'highlight');
      } else {
        label.classList.add('active', 'highlight');
      }
    } else if (e.type === 'blur') {
      if (input.value === '') {
        label.classList.remove('active', 'highlight');
      } else {
        label.classList.remove('highlight');
      }
    } else if (e.type === 'focus') {
      if (input.value === '') {
        label.classList.remove('highlight');
      } else {
        label.classList.add('highlight');
      }
    }
  }

  document.querySelectorAll('.tab a.a-login').forEach(function (tabLink) {
    tabLink.addEventListener('click', function (e) {
      e.preventDefault();

      let li = tabLink.parentElement;
      li.classList.add('active');
      li.parentElement.querySelectorAll('li').forEach(el => {
        if (el !== li) el.classList.remove('active');
      });

      let target = document.querySelector(tabLink.getAttribute('href'));
      document.querySelectorAll('.tab-content > div').forEach(div => {
        if (div !== target) div.style.display = 'none';
      });

      target.style.display = 'block';
      target.style.opacity = 0;
      setTimeout(() => {
        target.style.transition = 'opacity 0.6s';
        target.style.opacity = 1;
      }, 10);
    });
  });
});