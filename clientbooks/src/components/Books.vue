<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <b-alert
          :variant="variant"
          :show="dismissCountDown"
          dismissible
          @dismissed="dismissCountDown = 0"
          @dismiss-count-down="countDownChanged"
          >{{ message }}
        </b-alert>
        <button
          type="button"
          class="btn btn-success btn-sm"
          v-b-modal.book-modal
          @click="onShowModalInsert"
        >
          Adicionar Livro
        </button>
        <br />
        <br />
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="">Título</th>
              <th scope="col">Autor</th>
              <th scope="col">Descrição</th>
            </tr>
          </thead>
          <tbody v-for="(user, id) in users" :key="id">
            <tr v-for="(book, index) in user.books" :key="index">
              <td>{{ book.title }}</td>
              <td>{{ user.username }}</td>
              <td>{{ book.description }}</td>
              <td></td>
              <td>
                <div class="btn-group" role="group">
                  <button
                    type="button"
                    class="btn btn-warning btn-sm"
                    v-b-modal.book-modal
                    @click="editBook(book)"
                  >
                    Editar
                  </button>
                  <b-button
                    type="button"
                    class="btn btn-danger btn-sm"
                    @click="onShowDelete(book.id)"
                  >
                    Remover
                  </b-button>
                </div>
              </td>
            </tr>
            <b-modal id="modal-del" hide-footer>
              <template>
                Excluir Livro?
              </template>
              <div class="d-block text-center">
                <button type="button" class="btn btn-danger btn-lg" @click="onDeleteBook">
                  Excluir
                </button>
              </div>
            </b-modal>
          </tbody>
        </table>
        <b-alert show="show" variant="danger" v-if="this.users.length === 0">
          Você não possui livros adicionados.</b-alert
        >
      </div>
    </div>
    <b-modal ref="BookModal" id="book-modal" :title="tituloModal" hide-footer>
      <b-form @submit="onSubmit" @reset="onResetUpdate" class="w-100">
        <b-form-group id="form-title-edit-group" label="Título:" label-for="form-title-edit-input">
          <b-form-input
            id="form-title-edit-input"
            type="text"
            v-model="BookForm.title"
            required
            placeholder="Insira o título"
          >
          </b-form-input>
        </b-form-group>
        <b-form-group
          id="form-author-edit-group"
          label="Descrição:"
          label-for="form-author-edit-input"
        >
          <b-form-input
            id="form-author-edit-input"
            type="text"
            v-model="BookForm.description"
            required
            placeholder="Insira a descrição"
          >
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-read-edit-group">
          <select v-if="tituloModal !== 'Alterar'" required="true" v-model="userLogged">
            <option disabled value="">Escolha um usuário</option>
            <option v-for="(user, id) in users" :key="id" :label="user.username">{{
              user.id
            }}</option>
          </select>
          <select v-if="tituloModal == 'Alterar'" required="true" v-model="BookForm.id">
            <option disabled value="">Escolha um usuário</option>
            <option v-for="(user, id) in users" :key="id" :label="user.username">{{
              user.id
            }}</option>
          </select>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">{{ botao }}</b-button>
          <b-button type="reset" variant="danger">Cancelar</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
  </div>
</template>
<script>
import axios from 'axios';

export default {
  data() {
    return {
      users: [],
      userbooks: '',
      userLogged: '',
      BookForm: {
        id: 'Null',
        title: '',
        description: '',
      },
      message: '',
      bookId: '',
      showMessage: false,
      dismissCountDown: 0,
      tituloModal: '',
      variant: '',
      botao: '',
    };
  },
  components: {},
  methods: {
    onShowDelete(bookId) {
      this.bookId = bookId;
      this.$bvModal.show('modal-del');
    },
    onShowModalInsert() {
      this.tituloModal = 'Adicionar Livro';
      this.botao = 'Adicionar';
      this.BookForm.description = '';
      this.getUsers();
      this.initForm();
    },
    showAlert(message, variant) {
      this.dismissCountDown = 5;
      this.variant = variant;
      this.message = message;
    },
    countDownChanged(dismissCountDown) {
      this.dismissCountDown = dismissCountDown;
    },
    test() {
      this.removeBook(this.userLogged);
    },
    getUser(userId) {
      const path = `http://127.0.0.1:8000/users/${userId}`;
      axios
        .get(path)
        .then((res) => {
          this.userLogged = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
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
    addBook(payload, userLogged) {
      const path = `http://localhost:8000/books/${userLogged}/book`;
      axios
        .post(path, payload)
        .then(() => {
          this.getUsers();
          this.showAlert('Livro Adicionado!', 'info');
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getUsers();
        });
    },
    updateBook(payload, BookFormId) {
      const path = `http://localhost:8000/book/update/${BookFormId}`;
      axios
        // eslint-disable-next-line
        .put(path, payload)
        .then(() => {
          this.getUsers();
          this.showAlert('Livro Atualizado!', 'primary');
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getUsers();
        });
    },
    initForm() {
      this.BookForm.title = '';
      this.BookForm.author = '';
      this.BookForm.id = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.BookModal.hide();
      const payload = {
        title: this.BookForm.title,
        description: this.BookForm.description,
      };
      if (this.tituloModal === 'Adicionar Livro') {
        this.BookForm.title = '';
        this.BookForm.description = '';
        this.addBook(payload, this.userLogged);
      } else {
        this.updateBook(payload, this.BookForm.id);
      }
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.BookModal.hide();
      this.initForm();
    },
    editBook(user) {
      this.tituloModal = 'Alterar';
      this.botao = 'Atualizar';
      this.BookForm = user;
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.BookModal.hide();
      this.initForm();
      this.getUsers();
    },
    removeBook(bookID) {
      const path = `http://localhost:8000/book/delete/${bookID}`;
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
    onDeleteBook() {
      this.removeBook(this.bookId);
      this.$bvModal.hide('modal-del');
    },
  },
  created() {
    this.getUsers();
  },
};
</script>
