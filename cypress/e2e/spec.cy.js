describe('Home page spec', () => {  it('deployed react app to localhost', () => {    cy.visit('http://localhost:3000'),    cy.contains('Nombre d’utilisateurs : Chargement...')  }) })
describe('API /users', () => {
  beforeEach(() => {
    // Interception propre avec un alias
    cy.intercept('GET', '/users', {
      statusCode: 200,
      body: {
        utilisateurs: [
          [1, "Zaher", "zaher.madi@ynov.fr"],
          [2, "Test", "test@example.fr"]
        ]
      }
    }).as('getUsers')
  })

  it('affiche le bon nombre d’utilisateurs', () => {
    cy.visit('http://localhost:3000')

    cy.wait('@getUsers')

    cy.contains('Nombre d’utilisateurs : 2')
  })
})

 describe('Formulaire', () => {
  beforeEach(() => {
    cy.visit('http://localhost:3000');
  });

  it('remplit et valide le formulaire', () => {
    // Champs invalides au début
    cy.get('button[type="submit"]').should('be.disabled');

    // Nom
    cy.get('#lastName').type('Dupont');
    // Prénom
    cy.get('#firstName').type('Jean');
    // Date de naissance (plus de 18 ans)
    cy.get('#birthDate').type('1990-01-01');
    // Code postal
    cy.get('#postalCode').type('75000');
    // Ville
    cy.get('#city').type('Paris');
    // Email
    cy.get('#email').type('jean.dupont@example.com');

    // Soumettre
    cy.get('button[type="submit"]').should('not.be.disabled').click();

    // ✅ Message attendu (via alert ou autre)
    cy.on('window:alert', (str) => {
      expect(str).to.equal('✅ Inscription réussie !');
    });

    // Vérifie que les champs sont reset
    cy.get('#firstName').should('have.value', '');
    cy.get('#lastName').should('have.value', '');
    cy.get('#email').should('have.value', '');
  });
});
