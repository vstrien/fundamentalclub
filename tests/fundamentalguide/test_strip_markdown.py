import json
from fundamentalclub.fundamentalguide.guide import strip_markdown

def test_strip_markdown_should_produce_correctly_parsable_markdown():
    json_input = """
    ```json
{
  'risks': [
    {
      'indicator': 'Revenue',
      'description': 'The total amount of money a company makes from selling goods or services.',
      'sources': ['Income Statement'],
      'importance': 'High',
      'formula': 'Total Sales - Returns',
      'formula_components': [
        {
          'component': 'Total Sales',
          'source': 'Income Statement',
          'aliases': ['Sales', 'Net Sales']
        },
        {
          'component': 'Returns',
          'source': 'Income Statement',
          'aliases': ['Refunds']
        }
      ]
    },
    {
      'indicator': 'Gross Margin',
      'description': 'A measure of the company\'s manufacturing and distribution efficiency during the production process.',
      'sources': ['Income Statement'],
      'importance': 'High',
      'formula': '(Revenue - Cost of Goods Sold) / Revenue',
      'formula_components': [
        {
          'component': 'Revenue',
          'source': 'Income Statement',
          'aliases': []
        },
        {
          'component': 'Cost of Goods Sold',
          'source': 'Income Statement',
          'aliases': ['COGS']
        }
      ]
    },
    {
      'indicator': 'Operating Margin',
      'description': 'Indicates what proportion of a company\'s revenue is left over after paying for variable costs of production such as wages and raw materials.',
      'sources': ['Income Statement'],
      'importance': 'High',
      'formula': '(Operating Income / Revenue) * 100',
      'formula_components': [
        {
          'component': 'Operating Income',
          'source': 'Income Statement',
          'aliases': []
        },
        {
          'component': 'Revenue',
          'source': 'Income Statement',
          'aliases': []
        }
      ]
    },
    {
      'indicator': 'Debt-to-Equity Ratio',
      'description': 'A measure of a company\'s financial leverage, calculated by dividing its total liabilities by stockholders\' equity.',
      'sources': ['Balance Sheet'],
      'importance': 'High',
      'formula': 'Total Liabilities / Total Shareholders\' Equity',
      'formula_components': [
        {
          'component': 'Total Liabilities',
          'source': 'Balance Sheet',
          'aliases': []
        },
        {
          'component': 'Total Shareholders\' Equity',
          'source': 'Balance Sheet',
          'aliases': ['Shareholders\' Equity', 'Owner\'s Equity']
        }
      ]
    },
    {
      'indicator': 'Return on Equity',
      'description': 'A measure of the profitability of a business in relation to the equity.',
      'sources': ['Income Statement', 'Balance Sheet'],
      'importance': 'High',
      'formula': 'Net Income / Average Shareholders\' Equity',
      'formula_components': [
        {
          'component': 'Net Income',
          'source': 'Income Statement',
          'aliases': []
        },
        {
          'component': 'Average Shareholders\' Equity',
          'source': 'Balance Sheet',
          'aliases': ['Average Equity']
        }
      ]
    }
  ]
}
```
"""
    stripped = strip_markdown(json_input)
    json.loads(stripped)