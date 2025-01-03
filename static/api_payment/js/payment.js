const stripe = Stripe('pk_test_51QLa58LKyV0zbNjruqDqJXdGeEf1VDtYfMKwpOUtKJwLJl4gmdufY0RX9cHCfg3Mp89EkwyEZoq2U1CvX6jYSfUj00hN8dcw65'); // Replace with your Stripe public key
const elements = stripe.elements();
const card = elements.create('card');
card.mount('#card-element');

const form = document.getElementById('payment-form');

form.addEventListener('submit', async (event) => {
    event.preventDefault();

    // Fetch the client secret from your backend
    const response = await fetch('/api/payment/client/3/create-payment/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ order_id: 12 }), // Replace with actual order ID
    });

    const { client_secret } = await response.json();

    const { paymentIntent, error } = await stripe.confirmCardPayment(client_secret, {
        payment_method: {
            card: card,
            billing_details: {
                name: 'Juan16', // Replace with actual cardholder name
            },
        },
    });

    if (error) {
        console.error(error.message);
    } else {
        if (paymentIntent.status === 'succeeded') {
            console.log('Payment succeeded!');
            // Redirect to a success page or show a success message
            window.location.href = '/payment-success/';
        }
        window.location.href = '/payment-canceled/';
    }
});
