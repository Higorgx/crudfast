<template>
  <div class="container">
    <h1>Livros</h1>
    <hr />
    <users @onDeleteuser="updateBooksOnUserDeleted" />
    <br />
    <books ref="books" />
    <br />
  </div>
</template>
<script>
import users from './user.vue';
import Books from './Books.vue';

export default {
  name: 'crud',
  data() {
    return {};
  },
  components: {
    users,
    Books,
  },
  methods: {
    updateBooksOnUserDeleted() {
      this.$refs.books.getUsers();
    },
  },
  created() {},
};
</script>
