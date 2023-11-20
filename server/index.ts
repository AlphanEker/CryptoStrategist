import express, { Express, Request, Response } from 'express';
import {specs} from './swaggerConfig'; // Update the import statement
import swaggerUi from 'swagger-ui-express';

const app: Express = express();
const port = 8180;

// Middleware to parse JSON in request body
app.use(express.json());
// Serve Swagger UI
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(specs));

/**
 * @swagger
 * /:
 *   get:
 *     description: Main screen, this is for test purposes only.
 *     responses:
 *       200:
 *         description: Successful response
 */
app.get('/', (req: Request, res: Response) => {
  res.send('Express + TypeScript Serve');
});

/**
 * @swagger
 * /GetRate:
 *   get:
 *     description: Get Current Exchange Rate of the coin
 *     responses:
 *       200:
 *         description: Successful response
 */
// Get Current Exchange Rate
app.get('/GetRate', (req: Request, res: Response) => {
  res.send('500');
});

/**
 * @swagger
 * /UpdateRate:
 *   put:
 *     description: Update Exchange Rate of the coin
 *     responses:
 *       200:
 *         description: Successful response
 */
// Update Exchange Rate
app.get('/UpdateRate', (req: Request, res: Response) => {
  res.send('600');
});

/**
 * @swagger
 * /UpdateBalance:
 *   put:
 *     description: Update the balance of Agents
 *     responses:
 *       200:
 *         description: Successful response
 */
// Update Balance
app.post('/UpdateBalance', (req: Request, res: Response) => {
  // Assuming you send JSON with { "balance": newBalance } in the request body
  const newBalance: number = req.body.balance;
  // Logic to update the balance in your system
  // ...

  res.send(`Balance updated to ${newBalance}`);
});

/**
 * @swagger
 * /Buy:
 *   put:
 *     description: Buy the coin for given amount and update the coin balance
 *     responses:
 *       200:
 *         description: Successful response
 */
// Buy
app.post('/Buy', (req: Request, res: Response) => {
  // Assuming you send JSON with { "amount": buyAmount, "price": buyPrice } in the request body
  const buyAmount: number = req.body.amount;
  const buyPrice: number = req.body.price;
  // Logic to execute buy order
  // ...

  res.send(`Bought ${buyAmount} at ${buyPrice}`);
});

/**
 * @swagger
 * /Sell:
 *   get:
 *     description: Buy the coin for given amount and update the coin balance
 *     responses:
 *       200:
 *         description: Successful response
 */
// Sell
app.post('/Sell', (req: Request, res: Response) => {
  // Assuming you send JSON with { "amount": sellAmount, "price": sellPrice } in the request body
  const sellAmount: number = req.body.amount;
  const sellPrice: number = req.body.price;
  // Logic to execute sell order
  // ...

  res.send(`Sold ${sellAmount} at ${sellPrice}`);
});

/**
 * @swagger
 * /UpdateCoinBalance:
 *   get:
 *     description: Update The coin balance, this can be removed
 *     responses:
 *       200:
 *         description: Successful response
 */
// Update Coin Balance
app.post('/UpdateCoinBalance', (req: Request, res: Response) => {
  // Assuming you send JSON with { "coin": "BTC", "balance": newCoinBalance } in the request body
  const coin: string = req.body.coin;
  const newCoinBalance: number = req.body.balance;
  // Logic to update the coin balance in your system
  // ...

  res.send(`Updated ${coin} balance to ${newCoinBalance}`);
});

app.listen(port, () => {
  console.log(`⚡️[server]: Server is running at http://localhost:${port}`);
});
