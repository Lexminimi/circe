<template>
  <div class="quick-actions">
    <RouterLink to="/groups"><div class="action note">Groups</div></RouterLink>
    <RouterLink to="/groups"><div class="action task">Payment</div></RouterLink>
  </div>
</template>

<style>
.quick-actions {
  display: flex;
  justify-content: space-around;
  padding: 20px 0;
}

.action {
  display: inline-block;
  padding: 20px;
  width: 120px;
  text-align: center;
  border-radius: 10px;
  color: #fff;
}

.note {
  background-color: #43a047;
}

.task {
  background-color: #7e57c2;
}
</style>
