<template>
  <div>
    <div
      class="alert"
      :class="`alert-${status}`"
      role="alert"
    >
      {{ message }}
    </div>
    <br>
  </div>
</template>

<script>
export default {
  name: 'StatusAlert',
  props: {
    message: {
      type: String,
      required: true,
    },
    status: {
      type: String,
      required: true,
    },
  },
};
</script>
