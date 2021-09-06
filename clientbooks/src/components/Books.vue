<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Livros</h1>
        <hr />
        <br />
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
        <br/>
        <br/>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Título</th>
              <th scope="col">Autor</th>
              <th scope="col">Lido?</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(book, index) in books" :key="index">
              <td>{{ book.title }}</td>
              <td @click="getAutor(book.owner_id)">{{ book.owner_id }}</td>
              <td>{{BookForm.username}}</td>
              <td>
                <span v-if="book.read">Sim</span>
                <span v-else>Não</span>
              </td>
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
        <b-alert show="show" variant="danger" v-if="this.books.length === 0">
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
        <b-form-group id="form-author-edit-group" label="Autor:" label-for="form-author-edit-input">
          <b-form-input
            id="form-author-edit-input"
            type="text"
            v-model="BookForm.author"
            required
            placeholder="Insira o autor"
          >
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-read-edit-group">
          <b-form-checkbox v-model="BookForm.read" value="true">Lido?</b-form-checkbox>
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
      books: [],
      BookForm: {
        id: 'Null',
        title: '',
        author: '',
        read: false,
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
    getAutor(ownerId) {
      const path = `http://127.0.0.1:8000/users/${ownerId}`;
      axios
        .get(path)
        .then((res) => {
          this.BookForm = res.data;
          console.log(this.BookForm);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getBooks() {
      const path = 'http://127.0.0.1:8000/books';
      axios
        .get(path)
        .then((res) => {
          this.books = res.data;
          console.log(this.books.owner_id);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addBook(payload) {
      const path = 'http://localhost:5000/books';
      axios
        .post(path, payload)
        .then(() => {
          this.getBooks();
          this.showAlert('Livro Adicionado!', 'info');
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getBooks();
        });
    },
    updateBook(payload, bookID) {
      const path = `http://localhost:5000/books/${bookID}`;
      axios
        .put(path, payload)
        .then(() => {
          this.getBooks();
          this.showAlert('Livro Atualizado!', 'primary');
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getBooks();
        });
    },
    initForm() {
      this.BookForm.title = '';
      this.BookForm.author = '';
      this.BookForm.read = false;
      this.BookForm.id = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.BookModal.hide();
      let read = false;
      if (this.BookForm.read) {
        read = true;
      }
      const payload = {
        title: this.BookForm.title,
        author: this.BookForm.author,
        read,
      };
      if (this.tituloModal === 'Adicionar Livro') {
        this.addBook(payload);
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
    editBook(book) {
      this.tituloModal = 'Alterar';
      this.botao = 'Atualizar';
      this.BookForm = book;
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.BookModal.hide();
      this.initForm();
      this.getBooks();
    },
    removeBook(bookID) {
      const path = `http://localhost:5000/books/${bookID}`;
      axios
        .delete(path)
        .then(() => {
          this.getBooks();
          this.showAlert('Livro Removido!', 'danger');
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getBooks();
        });
    },
    onDeleteBook() {
      this.removeBook(this.bookId);
      this.$bvModal.hide('modal-del');
    },
  },
  created() {
    this.getBooks();
  },
};
</script>
