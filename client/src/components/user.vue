<template>
  <div class="container">
    <div class="row">
      <button
        type="button"
        class="btn btn-warning btn-sm"
        v-b-modal.user-modal
        @click="onShowModalInsert"
      >
        Adicionar Usuário
      </button>
      <hr />
      <select v-model="userLogged">
        <option disabled value="">Escolha um usuário</option>
        <option v-for="(user, id) in users" :key="id" :label="user.username">{{ user.id }}</option>
      </select>
      <button
        :disabled="userLogged == ''"
        type="button"
        class="btn btn-danger btn-sm"
        @click="onDeleteuser(userLogged)"
      >
        Deletar Usuário
      </button>
      <button
        :disabled="userLogged == ''"
        type="button"
        class="btn btn-warning btn-sm"
        v-b-modal.user-modal
        @click="onShowModalupdate(userLogged)"
      >
        Editar Usuário
      </button>
    </div>
    <div>
      <b-modal ref="userModal" id="user-modal" :title="tituloModal" hide-footer>
        <b-form @submit="onSubmit" @reset="onResetUpdate" class="w-100">
          <b-form-group id="form-title-edit-group" label="Nome:" label-for="form-title-edit-input">
            <b-form-input
              id="form-title-edit-input"
              type="text"
              v-model="userForm.username"
              required
              placeholder="Insira o nome"
            >
            </b-form-input>
          </b-form-group>
          <b-form-group
            id="form-author-edit-group"
            label="email:"
            label-for="form-author-edit-input"
          >
            <b-form-input
              id="form-author-edit-input"
              type="text"
              v-model="userForm.email"
              required
              placeholder="Insira o Email"
            >
            </b-form-input>
          </b-form-group>
          <b-button-group>
            <b-button type="submit" variant="primary">{{ button }}</b-button>
            <b-button type="reset" variant="danger">Cancelar</b-button>
          </b-button-group>
        </b-form>
      </b-modal>
    </div>
    <br>
     <b-alert
          :variant="variant"
          :show="dismissCountDown"
          dismissible
          @dismissed="dismissCountDown = 0"
          @dismiss-count-down="countDownChanged"
          >{{ message }}
        </b-alert>
  </div>
</template>
<script>
import axios from 'axios';

export default {
  name: 'User',
  data() {
    return {
      message: '',
      bookId: '',
      showMessage: false,
      dismissCountDown: 0,
      tituloModal: '',
      variant: '',
      users: [],
      userLogged: '',
      button: '',
      userForm: {
        id: 'Null',
        username: '',
        email: '',
        password: '',
      },
    };
  },
  methods: {
    onShowModalInsert() {
      this.tituloModal = 'Adicionar Usuário';
      this.button = 'Adicionar';
      this.getUsers();
      this.initForm();
    },
    onShowModalupdate() {
      this.tituloModal = 'Editar Usuário';
      this.button = 'Alterar';
      this.$emit('onDeleteuser');
      // eslint-disable-next-line
      const filter = this.users.filter((user) => user.id == this.userLogged)[0];
      this.userForm.username = filter.username;
      this.userForm.email = filter.email;
    },
    showAlert(message, variant) {
      this.dismissCountDown = 5;
      this.variant = variant;
      this.message = message;
    },
    countDownChanged(dismissCountDown) {
      this.dismissCountDown = dismissCountDown;
    },
    getUsers() {
      const path = 'http://127.0.0.1:8000/users';
      axios
        .get(path)
        .then((res) => {
          this.users = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getUser(id) {
      const path = `http://127.0.0.1:8000/users/${id}`;
      axios
        .get(path)
        .then((res) => {
          this.users = res.data;
          return this.users;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    adduser(payload) {
      const path = 'http://localhost:8000/users/';
      axios
        .post(path, payload)
        .then(() => {
          this.getUsers();
          this.showAlert('Usuário Adicionado!', 'info');
          this.showMessage = true;
          this.getUsers();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getUsers();
        });
    },
    initForm() {
      this.userForm.username = '';
      this.userForm.email = '';
      this.userForm.password = '123';
      this.userForm.id = '';
    },
    updateuser(payload, userLogged) {
      const path = `http://localhost:8000/user/update/${userLogged}`;
      axios
        .put(path, payload)
        .then(() => {
          this.getUsers();
          this.showAlert('Usuario Alterado!', 'info');
          this.showMessage = true;
          this.getUsers();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getUsers();
        });
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.userModal.hide();
      const payload = {
        username: this.userForm.username,
        email: this.userForm.email,
        password: this.userForm.password,
      };
      if (this.tituloModal === 'Adicionar Usuário') {
        this.adduser(payload);
      } else {
        this.updateuser(payload, this.userLogged);
        this.$emit('onDeleteuser');
      }
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.userModal.hide();
      this.initForm();
    },
    edituser(user) {
      this.tituloModal = 'Alterar';
      this.button = 'Atualizar';
      this.userForm = user;
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.userModal.hide();
      this.initForm();
      this.getUsers();
      this.userLogged = '';
    },
    removeUser(userID) {
      const path = `http://localhost:8000/user/delete/${userID}`;
      axios
        .delete(path)
        .then(() => {
          this.getUsers();
          this.showAlert('Livro Removido!', 'danger');
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getUsers();
        });
    },

    onDeleteuser(userId) {
      this.removeUser(userId);
      this.getUsers();
      this.$emit('onDeleteuser');
    },
  },
  created() {
    this.getUsers();
  },
};
</script>
