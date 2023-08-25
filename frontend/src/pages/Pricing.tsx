import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
  } from "@/components/ui/card"
  import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
  } from "@/components/ui/table"
   
  const pricingData = [
    {
        name: 'CPU',
        pricePerSeconds: 0.0111,
    },
    {
        name: 'NVIDIA T4',
        pricePerSeconds: 0.012,
    },
    {
        name: 'NVIDIA P100',
        pricePerSeconds: 0.0144,
    },
]
   
  export default function Pricing() {
    return (
        <div className="flex h-screen">
            <div className="m-auto">
        <Card className="w-[500px]">
            <CardHeader>
            <CardTitle>Compute Costs</CardTitle>
            <CardDescription>Pay only for what you use</CardDescription>

        </CardHeader>
      <CardContent>

        
        <Table>
            <TableHeader>
            <TableRow className="pointer-events-none">
                <TableHead className="w-[100px]"></TableHead>
                <TableHead className="text-right">Price per Seconds</TableHead>
            </TableRow>
            </TableHeader>
            <TableBody>
            {pricingData.map((data) => (
                <TableRow key={data.name}>
                <TableCell className="font-medium">{data.name}</TableCell>
                <TableCell className="text-right">${data.pricePerSeconds} / sec</TableCell>
                </TableRow>
            ))}
            </TableBody>
        </Table>
      </CardContent>

      </Card>
        </div>
        </div>
    )
  }

