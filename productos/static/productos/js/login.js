<script>
  const openBtn = document.getElementById('openSidebar');
  const closeBtn = document.getElementById('closeSidebar');
  const sidebar = document.getElementById('sidebar');

  openBtn.addEventListener('click', () => {
    sidebar.classList.remove('translate-x-full');
  });

  closeBtn.addEventListener('click', () => {
    sidebar.classList.add('translate-x-full');
  });
</script>
